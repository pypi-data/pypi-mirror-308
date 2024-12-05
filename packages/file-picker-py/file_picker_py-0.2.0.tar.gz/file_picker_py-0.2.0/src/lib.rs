use pyo3::prelude::*;
use rfd::FileDialog;

#[pyfunction]
pub fn pick_file_blocking() -> PyResult<Option<String>> {
        let file = FileDialog::new()
            .pick_file();

        match file {
            Some(file) => Ok(Some(pathbuf_to_string(&file))),
            None => Ok(None),
        }
}


#[pyfunction]
pub fn pick_files_blocking() -> PyResult<Vec<String>> {
    let files = FileDialog::new()
        .pick_files();

    match files {
        Some(files) => Ok(files.iter().map(|file| pathbuf_to_string(file)).collect()),
        None => Ok(vec![]),
    }
}

#[pyfunction]
pub fn pick_folder_blocking() -> PyResult<Option<String>> {
        let folder = FileDialog::new()
            .pick_folder();

        match folder {
            Some(folder) => Ok(Some(pathbuf_to_string(&folder))),
            None => Ok(None),
        }
}


#[pyfunction]
pub fn pick_folders_blocking() -> PyResult<Vec<String>> {
    let folders = FileDialog::new()
        .pick_folders();

    match folders {
        Some(folders) => Ok(folders.iter().map(|folder| pathbuf_to_string(folder)).collect()),
        None => Ok(vec![]),
    }
}

#[pyfunction]
pub fn pick_save_file_blocking() -> PyResult<Option<String>> {
        let file = FileDialog::new()
            .save_file();

        match file {
            Some(file) => Ok(Some(pathbuf_to_string(&file))),
            None => Ok(None),
        }
}


/// A Python module implemented in Rust.
#[pymodule]
mod file_picker_py {
    #[pymodule_export]
    use super::{pick_file_blocking, pick_files_blocking, pick_folder_blocking, pick_folders_blocking, pick_save_file_blocking};
}


fn pathbuf_to_string(path: &std::path::PathBuf) -> String {
    path.to_string_lossy().to_string()
}