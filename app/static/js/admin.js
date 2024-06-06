import showToast from './utsails.js';

const ip = '127.0.0.1';
const port = '5000';
const url = `${ip}:${port}`;
var username = 'sergi';
var deleteVisible = false;
var mode = true;
var files_to_ingest = [];
var file_names_to_ingest = [];
var ingested_files = [];
var selected_files = [];
var reader;


var input = document.getElementById('search-input');

input.addEventListener('blur', function (event) {
    document.getElementById('search-label').style.display = 'block';
    document.getElementById('search-input').style.display = 'none';
    document.getElementById('search-btn').style.display = 'block';
    document.getElementById('reset-search-btn').click();
    document.getElementById('reset-search-btn').style.display = 'none';
});

document.getElementById('search-input').addEventListener('input', function () {
    var searchTerm = this.value.toLowerCase();
    var select = document.getElementById('file-list-ingested');
    var options = select.getElementsByTagName('option');

    for (var i = 0; i < options.length; i++) {
        var optionText = options[i].text.toLowerCase();
        if (optionText.includes(searchTerm)) {
            options[i].style.display = '';
        } else {
            options[i].style.display = 'none';
        }
    }
});


document.getElementById('input-file').addEventListener("change", selectFile)
function selectFile(event) {
    openFile(event.target.files);
    event.value = null;
}

document.getElementById('input-dir').addEventListener('change', selectDir)
function selectDir(event) {
    var fileList = event.target.files;
    console.log(fileList)
    openFile(fileList);
}


function openFile(files) {
    var ingested = [];
    var check = false;
    if (files.length > 0) {
        for (var file of files) {
            var file_name = file.name;
            if (ingested_files.includes(file_name)) {
                ingested.push(file_name);
                check = true;
            } else if (file_names_to_ingest.includes(file_name)) {
                continue;
            } else {
                file_names_to_ingest.push(file_name);
                files_to_ingest.push(file);
            }
        }
        setFilesPreIngest();
    }

    if (check) {
        var already_ingested = '';
        if (ingested.length > 1) {
            for (var i = 0; i < ingested.length; i++) {
                already_ingested += ingested[i] + ', ';
                if (i == ingested.length - 1) {
                    already_ingested += `${ingested[i]} ya han sido procesados `
                }
            }
            showToast(`Los archivos ${already_ingested}`, "success")
            // alert(`Los archivos ${already_ingested}`)
        } else {
            showToast(`Los archivos ${ingested[0]}`, "error")
            // alert(`El archivo ${ingested[0]} ya ha sido procesado`)
        }
    }
}

function setFilesPreIngest() {
    var fileListPre = document.getElementById('file-list-pre');
    fileListPre.innerHTML = '';
    file_names_to_ingest.forEach(function (name) {
        var listItem = document.createElement('li');
        listItem.textContent = name;
        listItem.className = 'pl-4 p-2 no-collapse'
        fileListPre.appendChild(listItem);
    });
}


document.getElementById('load-files').addEventListener("click", ingestFiles);
function ingestFiles() {
    console.log("hola")
    var loading = document.getElementById('loading');
    if (files_to_ingest.length == 0) {
        alert('No hay archivos para subir')
    } else {
        for (var file of files_to_ingest) {
            loading.style.display = 'flex';
            ingestFile(file, loading);
        }
    }
    setPreIngestFilesListEmpty
    ();
}

document.getElementById('reset-files').addEventListener('click', setPreIngestFilesListEmpty
)
function setPreIngestFilesListEmpty
() {
    console.log()
    var fileListPre = document.getElementById('file-list-pre');
    fileListPre.innerHTML = '';
    files_to_ingest = [];
    file_names_to_ingest = [];
}

// CARGAR ARCHIVOS
async function ingestFile(file, loading) {
    try {
        var formData = new FormData();
        formData.append('file', file); //ADDED
        var response = await fetch(`http://${url}/v1/ingest/file`, {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': username
            }
        });

        if (response.ok) {
            var responseData = await response.json();
            console.log(responseData);
            getIngestedFiles();
            loading.style.display = 'none';

        } else {
            console.error('Error al enviar el archivo:', response.status);
        }
    } catch (error) {
        console.error('Error al procesar la solicitud:', error);
    }
}


async function getIngestedFiles() {
    ingested_files = [];
    try {                           //ADDED
        var response = await fetch(`http://${url}/v1/ingest/file`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Authorization': username
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        var data = await response.json();
        data.forEach(function (fileName) {
            ingested_files.push(fileName);
        });
        setIngestedFiles();
    } catch (error) {
        console.error('Error al obtener archivos guardados:', error);
        alert('Error al obtener archivos guardados');
    }
}

document.getElementById("reset-search-btn").addEventListener("click", setIngestedFiles)
function setIngestedFiles() {
    var fileListElement = document.getElementById('file-list-ingested');
    fileListElement.innerHTML = '';
    var fragment = document.createDocumentFragment();
    ingested_files.forEach(function (name) {
        var listItem = document.createElement('option');
        listItem.textContent = name;
        listItem.value = name;
        listItem.className = 'list-group-item no-collapse'
        fragment.appendChild(listItem);

    });
    fileListElement.appendChild(fragment);
}


async function keepAlive() {
    try {
        var response = await fetch(`http://${url}/health`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        var data = await response.json();
        var status = data.status;
        if (status === 'ok') {
            console.log('Conexion establecida');
        }
    } catch (error) {
        console.error('Error al obtener conexion:', error);
        alert('Conexión perdida.');
    }
}

document.getElementById("reset-files-selected").addEventListener("click", clearSelectedFilesList)
function clearSelectedFilesList() {
    selected_files = [];
    var selectedList = document.getElementById('file-list-selected');
    selectedList.innerHTML = '';
}

document.getElementById("file-list-ingested").addEventListener("change", addToSelectedList);

function addToSelectedList(event){
    var selectedOptions = event.target.selectedOptions;
    var selectedValues = Array.from(selectedOptions).map(option => option.value);

    selectedValues.forEach(function(value) {
        if (!selected_files.includes(value)) {
            selected_files.push(value);
            var newListItem = document.createElement('li');
            newListItem.textContent = value;
            newListItem.className = 'pl-4 p-2 border no-collapse';
            newListItem.setAttribute('value', value);
            this.appendChild(newListItem);
        }
    });
}

document.getElementById("select-all-ingesteds").addEventListener("click", selectAllOptions)
function selectAllOptions() {
    ingested_files.forEach(function (value) {
        if (!selected_files.includes(value)) {
            selected_files.push(value);
            var newListItem = document.createElement('li');
            newListItem.textContent = value;
            newListItem.className = 'pl-4 p-2 border no-collapse';
            newListItem.setAttribute('value', value);
            this.appendChild(newListItem);
        }
    });
}

document.getElementById("confirm-delete-btn").addEventListener("click", deleteFiles)
async function deleteFiles() {
    var deleting = document.getElementById('deleting');
    if (selected_files.length === 0) {
        alert('No hay archivos seleccionados');
        deleteDialog();
    } else {
        for (var fileName of selected_files) {
            deleting.style.display = 'block';
            deleteFile(fileName, deleting)
        }
    }
    deleteDialog();
    clearSelectedFilesList();
}


async function deleteFile(file_name, deleting) {
    try {
        var response = await fetch(`http://${url}/v1/ingest/file`, {
            method: 'DELETE',
            body: JSON.stringify({
                fileName: file_name
            }),
            headers: {
                'Authorization': username
            }
        });

        if (response.ok) {
            getIngestedFiles();
            deleting.style.display = 'none';
        } else {
            deleting.style.display = 'none';
            throw new Error(`Error al eliminar el archivo ${doc_id}: ${response.status}`);
        }

    } catch (error) {
        console.error('Error al procesar la solicitud de eliminar:', error);
    }
}

// Se busca la respuesta para el input
document.getElementById('delete').addEventListener("click", deleteDialog)
function deleteDialog() {
    var del = document.getElementById('delete-files');
    var conf = document.getElementById('confirm-delete');

    if (selected_files.length > 0) {
        if (!deleteVisible) {
            del.style.display = 'none';
            conf.style.display = 'flex';
        } else {
            del.style.display = 'flex';
            conf.style.display = 'none';
        }
        deleteVisible = !deleteVisible;
    }
}

function seeSelected() {
    console.log('selected files:');
    for (var i = 0; i < selected_files.length; i++) {
        console.log(selected_files[i]);
    }
}


function seeIngested() {
    console.log('ingested files:');
    for (var i = 0; i < ingested_files.length; i++) {
        console.log(ingested_files[i]);
    }
}

document.getElementById('open-dir').addEventListener("click", function(){
    document.getElementById('input-dir').click();
})


document.getElementById("search-btn").addEventListener("click", searchFile)
function searchFile() {
    document.getElementById('search-label').style.display = 'none';
    document.getElementById('search-btn').style.display = 'none';
    document.getElementById('reset-search-btn').style.display = 'flex';


    var input = document.getElementById('search-input');
    input.style.display = 'flex'
    input.style.width = '0';
    input.style.opacity = '0';

    input.focus();
    setTimeout(function () {
        input.style.width = '100%';
        input.style.opacity = '1';
    }, 5);
}



// setInterval(keepAlive, 20000);
// getIngestedFiles();