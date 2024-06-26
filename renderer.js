"use strict";

const { app, BrowserWindow, screen } = require("electron");
const { spawn } = require('child_process');
const path = require('path');

process.env.FLASK_APP = './app/entrypoint.py';
const entrypointPath = path.join(__dirname, 'entrypoint.py');

// Inicia el servidor Flask como un proceso secundario
const flaskProcess = spawn('python', [entrypointPath], {
  cwd: __dirname
});
let mainWindow = null;

// Keep a global reference of the mainWindowdow object, if you don't, the mainWindowdow will
// // be closed automatically when the JavaScript object is garbage collected.
// let subpy = null;

// const PY_DIST_FOLDER = "dist-python"; // python distributable folder
// const PY_SRC_FOLDER = "app"; // path to the python source
// const PY_MODULE = "app/entrypoint.py"; // the name of the main module

if (require('electron-squirrel-startup')) app.quit();

// const isRunningInBundle = () => {
//   return require("fs").existsSync(path.join(__dirname, PY_DIST_FOLDER));
// };

// const getPythonScriptPath = () => {
//   if (!isRunningInBundle()) {
//     return path.join(__dirname, PY_SRC_FOLDER, PY_MODULE);
//   }
//   if (process.platform === "win32") {
//     return path.join(
//       __dirname,
//       PY_DIST_FOLDER,
//       PY_MODULE.slice(0, -3) + ".exe"
//     );
//   }
//   return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE);
// };


// const startPythonSubprocess = () => {
//   let script = getPythonScriptPath();
//   if (isRunningInBundle()) {
//     //execFile: Running Flask App Executable in Electron (app.exe)
//     subpy = require("child_process").execFile(script, []);
//   } else {
//     //Running Flask App As a Source Code (entrypoint.py)
//     subpy = require("child_process").spawn("python", [script]);
//   }
// };

// const killPythonSubprocesses = (main_pid) => {
//   const python_script_name = path.basename(getPythonScriptPath());
//   let cleanup_completed = false;
//   const psTree = require("ps-tree");
//   psTree(main_pid, function (err, children) {
//     let python_pids = children
//       .filter(function (el) {
//         return el.COMMAND == python_script_name;
//       })
//       .map(function (p) {
//         return p.PID;
//       });
//     // kill all the spawned python processes
//     python_pids.forEach(function (pid) {
//       process.kill(pid);
//     });
//     subpy = null;
//     cleanup_completed = true;
//   });
//   return new Promise(function (resolve, reject) {
//     (function waitForSubProcessCleanup() {
//       if (cleanup_completed) return resolve();
//       setTimeout(waitForSubProcessCleanup, 30);
//     })();
//   });
// };

const createMainWindow = () => {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  // Create the browser mainWindow
  mainWindow = new BrowserWindow({
    webPreferences: {
      nodeIntegration: false,
      // contextIsolation: true,  // Habilitar el aislamiento de contexto
    },
    width: width - 100,
    height: height - 100,
    // transparent: true, // transparent header bar
    icon: __dirname + "/icon.png",
    // fullscreen: true,
    // opacity:0.8,
    // darkTheme: true,
    // frame: false,
    resizeable: true,
  });

  // Load the index page
  mainWindow.loadURL("http://localhost:5000/");

  // Open the DevTools.
  //mainWindow.webContents.openDevTools();

  // Emitted when the mainWindow is closed.
  mainWindow.on("closed", function () {
    mainWindow = null;
  });
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", function () {
  flaskProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  flaskProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  flaskProcess.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
  createMainWindow();
});

// disable menu
app.on("browser-window-created", function (e, window) {
  window.setMenu(null);
});

// Quit process when all windows are closed.
app.on("window-all-closed", () => {
  if (flaskProcess) {
    flaskProcess.kill(); 
  }

  app.quit();
});

app.on("activate", () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  // if (subpy == null) {
  //   startPythonSubprocess();
  // }
  if (win === null) {
    createMainWindow();
  }
});

app.on("quit", function () {
  // do some additional cleanup
});