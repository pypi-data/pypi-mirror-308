use std::io::{self, prelude::*};
use std::path::PathBuf;
use std::{fs::File, path::Path};

use convlog::tenhou::{Log, RawLog};
use pyo3::create_exception;
use pyo3::exceptions::PyIOError;
use pyo3::{
    exceptions::{PyFileNotFoundError, PyValueError},
    prelude::*,
};
use serde_json as json;

mod convlog;

create_exception!(_convlog, TenhouLogParsingError, PyValueError);
create_exception!(_convlog, TenhouToMjaiError, PyValueError);
create_exception!(_convlog, JsonSerializationError, PyValueError);
create_exception!(_convlog, JsonParsingError, PyValueError);

#[pyfunction]
fn tenhou_to_mjai(data: String) -> PyResult<Vec<String>> {
    let raw_log: RawLog = json::from_str(&data)
        .map_err(|_| JsonParsingError::new_err("failed to parse tenhou.net/6 log"))?;
    let log = Log::try_from(raw_log).map_err(|_| TenhouLogParsingError::new_err("invalid log"))?;
    let events = convlog::tenhou_to_mjai(&log)
        .map_err(|_| TenhouToMjaiError::new_err("failed to convert tenhou.net/6 log to mjai"))?;

    let mut ret = Vec::new();
    for event in &events {
        let to_push = json::to_string(event)
            .map_err(|_| JsonSerializationError::new_err("failed to serialize"))?;
        ret.push(to_push);
    }

    Ok(ret)
}

#[pyfunction]
#[pyo3(signature = (filename, mjai_out=None))]
fn tenhou_file_to_mjai(filename: PathBuf, mjai_out: Option<PathBuf>) -> PyResult<Vec<String>> {
    let mut file = File::open(&filename).map_err(|_| {
        PyFileNotFoundError::new_err(format!("failed to open tenhou.net/6 log file {filename:?}"))
    })?;
    let mut body = String::new();
    file.read_to_string(&mut body)?;
    let raw_log: RawLog = json::from_str(&body)
        .map_err(|_| JsonParsingError::new_err("failed to parse tenhou.net/6 log"))?;

    let log = Log::try_from(raw_log).map_err(|_| TenhouLogParsingError::new_err("invalid log"))?;

    let events = convlog::tenhou_to_mjai(&log)
        .map_err(|_| TenhouToMjaiError::new_err("failed to convert tenhou.net/6 log to mjai"))?;

    let mut ret = Vec::new();
    for event in &events {
        let to_push = json::to_string(event)
            .map_err(|_| JsonSerializationError::new_err("failed to serialize"))?;
        ret.push(to_push);
    }

    if let Some(mjai_out) = mjai_out {
        let mut w: Box<dyn Write> = if mjai_out == Path::new("-") {
            Box::from(io::stdout())
        } else {
            let mjai_out_file = File::create(&mjai_out).map_err(|_| {
                PyIOError::new_err(format!(
                    "failed to create mjai out file {:}",
                    mjai_out.display()
                ))
            })?;
            Box::from(mjai_out_file)
        };

        for event in &ret {
            writeln!(w, "{event}")
                .map_err(|_| PyIOError::new_err("failed to write to mjai out file"))?;
        }
    }

    Ok(ret)
}

pub fn get_version() -> String {
    let version = env!("CARGO_PKG_VERSION").to_string();
    // cargo uses "1.0-alpha1" etc. while python uses "1.0.0a1", this is not full compatibility,
    // but it's good enough for now
    // see https://docs.rs/semver/1.0.9/semver/struct.Version.html#method.parse for rust spec
    // see https://peps.python.org/pep-0440/ for python spec
    // it seems the dot after "alpha/beta" e.g. "-alpha.1" is not necessary, hence why this works
    version.replace("-alpha", "a").replace("-beta", "b")
}

#[pymodule]
fn _convlog(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add(
        "TenhouLogParsingError",
        py.get_type_bound::<TenhouLogParsingError>(),
    )?;
    m.add(
        "TenhouToMjaiError",
        py.get_type_bound::<TenhouToMjaiError>(),
    )?;
    m.add(
        "JsonSerializationError",
        py.get_type_bound::<JsonSerializationError>(),
    )?;
    m.add("JsonParsingError", py.get_type_bound::<JsonParsingError>())?;
    m.add_function(wrap_pyfunction!(tenhou_file_to_mjai, m)?)?;
    m.add_function(wrap_pyfunction!(tenhou_to_mjai, m)?)?;
    let version = get_version();
    m.add("__version__", version.clone())?;
    // keep VERSION for compatibility
    m.add("VERSION", version)?;
    Ok(())
}
