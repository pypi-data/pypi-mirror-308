"use strict";
(self["webpackChunkjupyterFsspec"] = self["webpackChunkjupyterFsspec"] || []).push([["lib_index_js"],{

/***/ "./lib/FileManager.js":
/*!****************************!*\
  !*** ./lib/FileManager.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FileManagerComponent: () => (/* binding */ FileManagerComponent),
/* harmony export */   FileManagerWidget: () => (/* binding */ FileManagerWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);


// import { TreeComponent } from './Tree';
// import { SelectOptionComponent } from './SourceSelector';
// import { DebugPanel } from './DebugPanel';
const FileManagerComponent = () => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "hi"));
};
class FileManagerWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor() {
        super();
        this.addClass('jp-react-widget');
        this.addClass('jp-fsspec-widget');
        console.log('node is: ', this.node);
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(FileManagerComponent, null);
    }
}


/***/ }),

/***/ "./lib/FssFilesysItem.js":
/*!*******************************!*\
  !*** ./lib/FssFilesysItem.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FssFilesysItem: () => (/* binding */ FssFilesysItem)
/* harmony export */ });
/* harmony import */ var _treeContext__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./treeContext */ "./lib/treeContext.js");
// Element for displaying a single fsspec filesystem

// import { Logger } from "./logger"
const HOVER = 'var(--jp-layout-color3)';
const UNHOVER = 'var(--jp-layout-color2)';
const SELECTED = 'var(--jp-layout-color4)';
class FssFilesysItem {
    constructor(model, fsInfo, userClickSlots) {
        this._selected = false;
        this._hovered = false;
        this.model = model;
        this.filesysName = fsInfo.name;
        this.filesysType = fsInfo.type;
        this.fsInfo = fsInfo;
        this.clickSlots = [];
        for (const slot of userClickSlots) {
            this.clickSlots.push(slot);
        }
        let fsItem = document.createElement('div');
        fsItem.classList.add('jfss-fsitem-root');
        fsItem.addEventListener('mouseenter', this.handleFsysHover.bind(this));
        fsItem.addEventListener('mouseleave', this.handleFsysHover.bind(this));
        fsItem.dataset.fssname = fsInfo.name;
        this.root = fsItem;
        // Set the tooltip
        this.root.title = `Root Path: ${fsInfo.path}`;
        this.nameField = document.createElement('div');
        this.nameField.classList.add('jfss-fsitem-name');
        this.nameField.innerText = this.filesysName;
        fsItem.appendChild(this.nameField);
        this.pathField = document.createElement('div');
        this.pathField.classList.add('jfss-fsitem-type');
        this.pathField.innerText = 'Path: ' + fsInfo.path;
        fsItem.appendChild(this.pathField);
        fsItem.addEventListener('click', this.handleClick.bind(this));
        fsItem.addEventListener('contextmenu', this.handleContext.bind(this));
    }
    handleContext(event) {
        // Prevent ancestors from adding extra context boxes
        event.stopPropagation();
        // Prevent default browser context menu (unless shift pressed
        // as per usual JupyterLab conventions)
        if (!event.shiftKey) {
            event.preventDefault();
        }
        else {
            return;
        }
        // Make/add the context menu
        let context = new _treeContext__WEBPACK_IMPORTED_MODULE_0__.FssContextMenu(this.model);
        context.root.dataset.fss = this.root.dataset.fss;
        let body = document.getElementsByTagName('body')[0];
        body.appendChild(context.root);
        // Position it under the mouse (top left corner normally,
        // or bottom right if that corner is out-of-viewport)
        let parentRect = body.getBoundingClientRect();
        let contextRect = context.root.getBoundingClientRect();
        let xCoord = event.clientX - parentRect.x;
        let yCoord = event.clientY - parentRect.y;
        let spacing = 12;
        if (xCoord + contextRect.width > window.innerWidth || yCoord + contextRect.height > window.innerHeight) {
            // Context menu is cut off when positioned under mouse at top left corner,
            // use the bottom right corner instead
            xCoord -= contextRect.width;
            yCoord -= contextRect.height;
            // Shift the menu so the mouse is inside it, not at the corner/edge
            xCoord += spacing;
            yCoord += spacing;
        }
        else {
            // Shift the menu so the mouse is inside it, not at the corner/edge
            xCoord -= spacing;
            yCoord -= spacing;
        }
        context.root.style.left = `${xCoord}` + 'px';
        context.root.style.top = `${yCoord}` + 'px';
    }
    setMetadata(value) {
        this.root.dataset.fss = value;
    }
    set selected(value) {
        this._selected = value;
        if (value) {
            this.root.style.backgroundColor = SELECTED;
        }
        else {
            this.hovered = this._hovered;
        }
    }
    set hovered(state) {
        this._hovered = state;
        if (this._selected) {
            this.root.style.backgroundColor = SELECTED;
        }
        else {
            if (state) {
                this.root.style.backgroundColor = HOVER;
            }
            else {
                this.root.style.backgroundColor = UNHOVER;
            }
        }
    }
    handleFsysHover(event) {
        if (event.type == 'mouseenter') {
            this.hovered = true;
        }
        else {
            this.hovered = false;
        }
    }
    handleClick(_event) {
        this.selected = true;
        for (const slot of this.clickSlots) {
            slot(this.fsInfo);
        }
    }
}



/***/ }),

/***/ "./lib/FssTreeItem.js":
/*!****************************!*\
  !*** ./lib/FssTreeItem.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FssTreeItem: () => (/* binding */ FssTreeItem)
/* harmony export */ });
/* harmony import */ var _jupyter_web_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter/web-components */ "webpack/sharing/consume/default/@jupyter/web-components");
/* harmony import */ var _jupyter_web_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_web_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _treeContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./treeContext */ "./lib/treeContext.js");
/* harmony import */ var _logger__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./logger */ "./lib/logger.js");
// Element for displaying a single fsspec tree entry




class FssTreeItem {
    constructor(model, clickSlots, autoExpand, expandOnClickAnywhere) {
        this.isDir = false;
        this.pendingExpandAction = false;
        this.lazyLoadAutoExpand = true;
        this.clickAnywhereDoesAutoExpand = true;
        // The TreeItem component is the root and handles
        // tree structure functionality in the UI
        let root = new _jupyter_web_components__WEBPACK_IMPORTED_MODULE_0__.TreeItem();
        this.root = root;
        this.model = model;
        this.clickSlots = clickSlots;
        this.lazyLoadAutoExpand = autoExpand;
        this.clickAnywhereDoesAutoExpand = expandOnClickAnywhere;
        // Use a MutationObserver on the root TreeItem's shadow DOM,
        // where the TreeItem's expand/collapse control will live once
        // the item has children to show
        let observeOptions = {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class'],
            attributeOldValue: true,
        };
        this.treeItemObserver = new MutationObserver(this.handleDomMutation.bind(this));
        // The main container holds custom fsspec UI/functionality
        let container = document.createElement('div');
        container.classList.add('jfss-tree-item-container');
        root.appendChild(container);
        this.container = container;
        // Reserve space in the layout for the file/folder icon
        let dirSymbol = document.createElement('div');
        dirSymbol.classList.add('jfss-dir-symbol');
        container.appendChild(dirSymbol);
        dirSymbol.style.visibility = 'hidden';
        this.dirSymbol = dirSymbol;
        // Show the name of this file/folder (a single path segment)
        let nameLbl = document.createElement('div');
        container.appendChild(nameLbl);
        this.nameLbl = nameLbl;
        // Show the name of this file/folder (a single path segment)
        let sizeLbl = document.createElement('div');
        sizeLbl.classList.add('jfss-filesize-lbl');
        container.appendChild(sizeLbl);
        this.sizeLbl = sizeLbl;
        // Add click and right click handlers to the tree component
        root.addEventListener('contextmenu', this.handleContext.bind(this));
        root.addEventListener('click', this.handleClick.bind(this), true);
        // Start observing for changes to the TreeItem's shadow root
        if (this.root.shadowRoot) {
            this.treeItemObserver.observe(this.root.shadowRoot, observeOptions);
        }
    }
    appendChild(elem) {
        this.root.appendChild(elem);
    }
    setMetadata(user_path, size) {
        this.root.dataset.fss = user_path;
        this.root.dataset.fsize = size;
        let sizeDisplay = `(${size.toLocaleString()})`;
        // if (parseInt(size) > 100) {
        //     const sizeFormat = new Intl.NumberFormat(undefined, {
        //         notation: 'scientific',
        //     });
        //     sizeDisplay = `(${sizeFormat.format(parseInt(size))})`;
        // }
        this.sizeLbl.innerText = sizeDisplay;
    }
    setText(value) {
        this.nameLbl.innerText = value;
    }
    setType(symbol) {
        this.dirSymbol.replaceChildren();
        this.dirSymbol.style.visibility = 'visible';
        if (symbol == 'dir') {
            _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.folderIcon.element({ container: this.dirSymbol });
            this.isDir = true;
            this.sizeLbl.style.display = 'none';
        }
        if (symbol == 'file') {
            _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.fileIcon.element({ container: this.dirSymbol });
            this.isDir = false;
        }
    }
    handleDomMutation(records, observer) {
        // This is used to auto-expand directory-type TreeItem's to show children after
        // a lazy-load. It checks the TreeItem's shadow dom for the addition of an
        // "expand-collapse-button" child control which is used to expand and show
        // children (in the tree) of this class's root TreeItem node. By auto expanding here,
        // we save the user from having to click twice on a folder (once to lazy-load
        // and another time to expand) when they want to expand it
        if (this.lazyLoadAutoExpand && this.pendingExpandAction) {
            for (const rec of records) {
                let addedNodes = rec === null || rec === void 0 ? void 0 : rec.addedNodes;
                if (addedNodes) {
                    for (let node of addedNodes) {
                        if ((node === null || node === void 0 ? void 0 : node.classList) && node.classList.contains('expand-collapse-button')) {
                            node.click();
                            this.root.scrollTo();
                            this.pendingExpandAction = false;
                        }
                    }
                }
            }
        }
    }
    handleClick(event) {
        // Filter click events to handle this item's root+shadow and container
        if (event.target === this.root || this.container.contains(event.target) || this.root.shadowRoot.contains(event.target)) {
            // Handles normal click events on the TreeItem (unlike the MutationObserver system
            // which is for handling folder auto-expand after lazy load)
            if (this.clickAnywhereDoesAutoExpand) {
                let expander = this.root.shadowRoot.querySelector('.expand-collapse-button');
                if (expander) {
                    let expRect = expander.getBoundingClientRect();
                    if ((event.clientX < expRect.left
                        || event.clientX > expRect.right
                        || event.clientY < expRect.top
                        || event.clientY > expRect.bottom)) {
                        _logger__WEBPACK_IMPORTED_MODULE_2__.Logger.debug('--> Click outside expander, force expander click');
                        expander.click();
                        this.root.scrollTo();
                    }
                }
            }
            // Fire connected slots that were supplied to this item on init
            if (this.isDir) {
                for (let slot of this.clickSlots) {
                    slot(this.root.dataset.fss);
                }
            }
            else {
                this.root.click();
            }
        }
    }
    expandItem() {
        // This method's purpose is to expand folder items to show children
        // after a lazy load, but when this is called, the expand controls aren't
        // ready...a flag is set here to indicate that an expand action is desired,
        // which is used by the MutationObserver member var's handler to find the
        // expand/collapse Element when it is added so that it can be click()'d
        this.pendingExpandAction = true;
    }
    handleContext(event) {
        // Prevent ancestors from adding extra context boxes
        event.stopPropagation();
        // Prevent default browser context menu (unless shift pressed
        // as per usual JupyterLab conventions)
        if (!event.shiftKey) {
            event.preventDefault();
        }
        else {
            return;
        }
        // Make/add the context menu
        let context = new _treeContext__WEBPACK_IMPORTED_MODULE_3__.FssContextMenu(this.model);
        context.root.dataset.fss = this.root.dataset.fss;
        let body = document.getElementsByTagName('body')[0];
        body.appendChild(context.root);
        // Position it under the mouse (top left corner normally,
        // or bottom right if that corner is out-of-viewport)
        let parentRect = body.getBoundingClientRect();
        let contextRect = context.root.getBoundingClientRect();
        let xCoord = event.clientX - parentRect.x;
        let yCoord = event.clientY - parentRect.y;
        let spacing = 12;
        if (xCoord + contextRect.width > window.innerWidth || yCoord + contextRect.height > window.innerHeight) {
            // Context menu is cut off when positioned under mouse at top left corner,
            // use the bottom right corner instead
            xCoord -= contextRect.width;
            yCoord -= contextRect.height;
            // Shift the menu so the mouse is inside it, not at the corner/edge
            xCoord += spacing;
            yCoord += spacing;
        }
        else {
            // Shift the menu so the mouse is inside it, not at the corner/edge
            xCoord -= spacing;
            yCoord -= spacing;
        }
        context.root.style.left = `${xCoord}` + 'px';
        context.root.style.top = `${yCoord}` + 'px';
    }
}


/***/ }),

/***/ "./lib/handler/fileOperations.js":
/*!***************************************!*\
  !*** ./lib/handler/fileOperations.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FsspecModel: () => (/* binding */ FsspecModel)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./handler */ "./lib/handler/handler.js");
/* harmony import */ var _logger__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../logger */ "./lib/logger.js");


class FsspecModel {
    constructor() {
        this.activeFilesystem = '';
        this.userFilesystems = {};
        this.retry = 0;
    }
    async initialize(automatic = true, retry = 3) {
        this.retry = retry;
        if (automatic) {
            // Perform automatic setup: Fetch filesystems from config and store
            // this model on the window as global application state
            this.storeApplicationState();
            // Attempt to read and store user config values
            this.userFilesystems = {};
            try {
                for (let i = 0; i < retry; i++) {
                    _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.info('[FSSpec] Attempting to read config file...');
                    let result = await this.getStoredFilesystems();
                    if ((result === null || result === void 0 ? void 0 : result.status) == 'success') {
                        // TODO report config entry errors
                        _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.info(`[FSSpec] Successfully retrieved config:${JSON.stringify(result)}`);
                        this.userFilesystems = result.filesystems;
                        // Set active filesystem to first
                        if (Object.keys(result).length > 0) {
                            this.activeFilesystem = Object.keys(this.userFilesystems)[0];
                        }
                        break;
                    }
                    else {
                        // TODO handle no config file
                        _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.error('[FSSpec] Error fetching filesystems from user config');
                        if (i + 1 < retry) {
                            _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.info('[FSSpec]   retrying...');
                        }
                    }
                }
            }
            catch (error) {
                _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.error(`[FSSpec] Error: Unknown error initializing fsspec model:\n${error}`);
            }
        }
    }
    // Store model on the window as global app state
    storeApplicationState() {
        window.fsspecModel = this;
    }
    // ====================================================================
    // FileSystem API calls
    // ====================================================================
    setActiveFilesystem(name) {
        this.activeFilesystem = name;
    }
    getActiveFilesystem() {
        return this.activeFilesystem;
    }
    getActiveFilesystemInfo() {
        return this.userFilesystems[this.activeFilesystem];
    }
    async refreshConfig() {
        // TODO fix/refactor
        this.userFilesystems = {};
        try {
            for (let i = 0; i < this.retry; i++) {
                _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.info('[FSSpec] Attempting to read config file...');
                let result = await this.getStoredFilesystems();
                if ((result === null || result === void 0 ? void 0 : result.status) == 'success') {
                    // TODO report config entry errors
                    _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.info(`[FSSpec] Successfully retrieved config:${JSON.stringify(result)}`);
                    this.userFilesystems = result.filesystems;
                    // Set active filesystem to first
                    if (Object.keys(result).length > 0) {
                        this.activeFilesystem = Object.keys(this.userFilesystems)[0];
                    }
                    break;
                }
                else {
                    // TODO handle no config file
                    _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.error('[FSSpec] Error fetching filesystems from user config');
                    if (i + 1 < this.retry) {
                        _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.info('[FSSpec]   retrying...');
                    }
                }
            }
        }
        catch (error) {
            _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.error(`[FSSpec] Error: Unknown error initializing fsspec model:\n${error}`);
        }
    }
    async getStoredFilesystems() {
        // Fetch list of filesystems stored in user's config file
        let filesystems = {};
        let result = {
            'filesystems': filesystems,
            'status': 'success',
        };
        try {
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)('config');
            _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.debug(`[FSSpec] Request config:\n${JSON.stringify(response)}`);
            if ((response === null || response === void 0 ? void 0 : response.status) == 'success' && (response === null || response === void 0 ? void 0 : response.content)) {
                for (const filesysInfo of response.content) {
                    if (filesysInfo === null || filesysInfo === void 0 ? void 0 : filesysInfo.name) {
                        _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.debug(`[FSSpec] Found filesystem: ${JSON.stringify(filesysInfo)}`);
                        filesystems[filesysInfo.name] = filesysInfo;
                    }
                    else {
                        // TODO better handling for partial errors
                        _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.error(`[FSSpec] Error, filesystem from config is missing a name: ${filesysInfo}`);
                    }
                }
            }
            else {
                _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.error(`[FSSpec] Error fetching config from server...`);
            }
            // // const fetchedFilesystems = response['content'];
            // // console.log(fetchedFilesystems);
            // // Map names to filesys metadata
            // for (const filesysInfo of fetchedFilesystems) {
            //   if ('name' in filesysInfo) {
            //     filesystems[filesysInfo.name] = filesysInfo;
            //   } else {
            //     console.error(
            //       `Filesystem from config is missing a name: ${filesysInfo}`
            //     );
            //   }
            // }
        }
        catch (error) {
            _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.error(`[FSSpec] Error: Unknown error fetching config:\n${error}`);
        }
        return result;
    }
    async getContent(key, item_path, type = '') {
        try {
            const query = new URLSearchParams({
                key,
                item_path,
                type
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`fsspec?${query.toString()}`, {
                method: 'GET'
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to fetch filysystems: ', error);
            return null;
        }
    }
    async getRangeContent(key, item_path, type = 'range', start, end) {
        try {
            const query = new URLSearchParams({
                key,
                item_path,
                type
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`fsspec?${query.toString()}`, {
                method: 'GET',
                headers: {
                    Range: `${start}-${end}`
                }
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to fetch filysystems: ', error);
            return null;
        }
    }
    async delete(key, item_path) {
        try {
            const reqBody = JSON.stringify({
                key,
                item_path
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)('fsspec', {
                method: 'DELETE',
                body: reqBody,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to delete: ', error);
            return null;
        }
    }
    async delete_refactored(key, item_path) {
        try {
            const query = new URLSearchParams({
                key,
                item_path
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`files?${query.toString()}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to delete: ', error);
            return null;
        }
    }
    async deleteDir(key, item_path) {
        try {
            const reqBody = JSON.stringify({
                key: key,
                item_path
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)('fsspec', {
                method: 'DELETE',
                body: reqBody,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to delete: ', error);
            return null;
        }
    }
    async post(key, item_path, content) {
        try {
            const query = new URLSearchParams({
                action: 'write'
            });
            const reqBody = JSON.stringify({
                key,
                item_path,
                content
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`fsspec?${query.toString()}`, {
                method: 'POST',
                body: reqBody,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to post: ', error);
            return null;
        }
    }
    async postDir(key, item_path, content, action = 'write') {
        try {
            console.log('postDir');
            const query = new URLSearchParams({
                action: action
            });
            const reqBody = JSON.stringify({
                key: key,
                item_path,
                content
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`fsspec?${query.toString()}`, {
                method: 'POST',
                body: reqBody,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to post: ', error);
            return null;
        }
    }
    // async update(
    //   key: any = 'local%7CSourceDisk%7C.',
    //   item_path = '',
    //   content = ''
    // ): Promise<any> {
    //   try {
    //     console.log('postDir');
    //     const reqBody = JSON.stringify({
    //       key: key,
    //       item_path:
    //         '/Users/rosioreyes/Desktop/notebooks/eg_notebooks/sample_dir',
    //       content: 'fsspec_generated_folder'
    //     });
    //     const response = await requestAPI<any>('fsspec', {
    //       method: 'PUT',
    //       body: reqBody,
    //       headers: {
    //         'Content-Type': 'application/json'
    //       }
    //     });
    //     console.log('response is: ', response);
    //   } catch (error) {
    //     console.error('Failed to post: ', error);
    //     return null;
    //   }
    // }
    /* TODO: modify, overwrites file entirely*/
    async update(key, item_path, content) {
        try {
            console.log('postDir');
            const reqBody = JSON.stringify({
                key,
                item_path,
                content
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)('fsspec', {
                method: 'PUT',
                body: reqBody,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to post: ', error);
            return null;
        }
    }
    async move(key = 'local%7CSourceDisk%7C.', item_path, content) {
        try {
            console.log('postDir');
            const query = new URLSearchParams({
                action: 'move'
            });
            const reqBody = JSON.stringify({
                key,
                item_path,
                content
            });
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`fsspec?${query.toString()}`, {
                method: 'POST',
                body: reqBody,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('response is: ', response);
        }
        catch (error) {
            console.error('Failed to post: ', error);
            return null;
        }
    }
    async listActiveFilesystem() {
        // Return list of files for active FS
        // Return list of cached file systems?
        if (!this.activeFilesystem) {
            throw new Error('No active filesystem set.');
        }
        try {
            return await this.walkDirectory(this.userFilesystems[this.activeFilesystem].key, 'find');
        }
        catch (error) {
            console.error('Failed to list currently active file system: ', error);
            return null;
        }
    }
    // ====================================================================
    // File and Directory API calls
    // ====================================================================
    async getFileContent(path, name) {
        const query = new URLSearchParams({
            path: path,
            name: name
        });
        try {
            return await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`fsspec?${query.toString()}`, {
                method: 'GET'
            });
        }
        catch (error) {
            console.error(`Failed to fetch file content at ${path}: `, error);
            return null;
        }
    }
    async walkDirectory(key, type = 'find', item_path = '') {
        let query = new URLSearchParams({ key, item_path });
        if (type !== '') {
            query = new URLSearchParams({ key, item_path, type });
        }
        try {
            return await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`fsspec?${query.toString()}`, {
                method: 'GET'
            });
        }
        catch (error) {
            console.error(`Failed to list filesystem ${key}: `, error);
            return null;
        }
    }
    async listDirectory(key, item_path = '', type = 'default') {
        const query = new URLSearchParams({ key, item_path, type }).toString();
        let result = null;
        _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.debug(`[FSSpec] Fetching files -> ${query}`);
        try {
            result = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`files?${query}`, {
                method: 'GET'
            });
        }
        catch (error) {
            _logger__WEBPACK_IMPORTED_MODULE_0__.Logger.error(`[FSSpec] Failed to list filesystem ${error}: `);
        }
        return result;
    }
    async updateFile(path, recursive = false, backend = 'local', content // Update function for different content
    ) {
        console.log('updateFile function');
        let requestBody;
        if (typeof content === 'string') {
            requestBody = content;
        }
        const query = new URLSearchParams({
            path: path,
            backend: backend,
            action: 'write',
            content: requestBody
        });
        console.log('endpoint is: ');
        console.log(`fsspec?${query.toString()}`);
        try {
            return await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)(`fsspec?${query.toString()}`, {
                method: 'POST'
            });
        }
        catch (error) {
            console.error(`Failed to update file at ${path}: `, path);
            return null;
        }
    }
    async copyFile(srcPath, destPath, recursive = false, backend = 'local') {
        const body = JSON.stringify({
            action: 'copy',
            path: srcPath,
            dest_path: destPath,
            recursive: recursive,
            backend: backend
        });
        try {
            return await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)('fsspec', {
                method: 'POST',
                body: body,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        }
        catch (error) {
            console.error(`Failed to copy file ${srcPath} to ${destPath}: `, error);
            return null;
        }
    }
}


/***/ }),

/***/ "./lib/handler/handler.js":
/*!********************************!*\
  !*** ./lib/handler/handler.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyter_fsspec', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var path__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! path */ "./node_modules/path-browserify/index.js");
/* harmony import */ var path__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(path__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _FileManager__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./FileManager */ "./lib/FileManager.js");
/* harmony import */ var _handler_fileOperations__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./handler/fileOperations */ "./lib/handler/fileOperations.js");
/* harmony import */ var _FssFilesysItem__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./FssFilesysItem */ "./lib/FssFilesysItem.js");
/* harmony import */ var _FssTreeItem__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./FssTreeItem */ "./lib/FssTreeItem.js");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyter_web_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyter/web-components */ "webpack/sharing/consume/default/@jupyter/web-components");
/* harmony import */ var _jupyter_web_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyter_web_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _logger__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./logger */ "./lib/logger.js");










class UniqueId {
    static get_id() {
        UniqueId._id_val += 1;
        return UniqueId._id_val;
    }
}
UniqueId._id_val = -1;
class FsspecWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor(model) {
        super();
        this.elementHeap = {}; // Holds FssTreeItem's keyed by path
        this.sourcesHeap = {}; // Holds FssFilesysItem's keyed by name
        this.dirTree = {};
        this.model = model;
        this.title.label = 'FSSpec';
        this.node.classList.add('jfss-root');
        let primaryDivider = document.createElement('div');
        primaryDivider.classList.add('jfss-primarydivider');
        this.upperArea = document.createElement('div');
        this.upperArea.classList.add('jfss-upperarea');
        let mainLabel = document.createElement('div');
        mainLabel.classList.add('jfss-mainlabel');
        mainLabel.innerText = 'Jupyter FSSpec';
        this.upperArea.appendChild(mainLabel);
        let sourcesControls = document.createElement('div');
        sourcesControls.classList.add('jfss-sourcescontrols');
        this.upperArea.appendChild(sourcesControls);
        let sourcesLabel = document.createElement('div');
        sourcesLabel.classList.add('jfss-sourceslabel');
        sourcesLabel.innerText = 'Configured Filesystems';
        sourcesLabel.title = 'A list of filesystems stored in the Jupyter FSSpec yaml';
        sourcesControls.appendChild(sourcesLabel);
        let sourcesDivider = document.createElement('div');
        sourcesLabel.classList.add('jfss-sourcesdivider');
        sourcesControls.appendChild(sourcesDivider);
        let refreshConfig = document.createElement('div');
        refreshConfig.title = 'Re-read and refresh sources from config';
        refreshConfig.classList.add('jfss-refreshconfig');
        refreshConfig.innerText = '\u{21bb}';
        refreshConfig.addEventListener('click', this.fetchConfig.bind(this));
        sourcesControls.appendChild(refreshConfig);
        this.filesysContainer = document.createElement('div');
        this.filesysContainer.classList.add('jfss-userfilesystems');
        this.upperArea.appendChild(this.filesysContainer);
        let hsep = document.createElement('div');
        hsep.classList.add('jfss-hseparator');
        let lowerArea = document.createElement('div');
        lowerArea.classList.add('jfss-lowerarea');
        // let browserAreaLabel = document.createElement('div');
        // browserAreaLabel.classList.add('jfss-browseAreaLabel');
        // browserAreaLabel.innerText = 'Browse Filesystem';
        // lowerArea.appendChild(browserAreaLabel);
        this.selectedFsLabel = document.createElement('div');
        this.selectedFsLabel.classList.add('jfss-selectedFsLabel');
        this.selectedFsLabel.innerText = '<Select a filesystem>';
        lowerArea.appendChild(this.selectedFsLabel);
        let resultArea = document.createElement('div');
        resultArea.classList.add('jfss-resultarea');
        lowerArea.appendChild(resultArea);
        this.treeView = new _jupyter_web_components__WEBPACK_IMPORTED_MODULE_4__.TreeView();
        resultArea.appendChild(this.treeView);
        primaryDivider.appendChild(this.upperArea);
        primaryDivider.appendChild(hsep);
        primaryDivider.appendChild(lowerArea);
        this.node.appendChild((primaryDivider));
        this.populateFilesystems();
    }
    async fetchConfig() {
        this.selectedFsLabel.innerText = '<Select a filesystem>';
        await this.model.refreshConfig();
        _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.debug(`[FSSpec] Refresh config:\n${JSON.stringify(this.model.userFilesystems)}`);
        this.populateFilesystems();
    }
    populateFilesystems() {
        _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.debug(`[FSSpec] Populate filesystems: \n${JSON.stringify(this.model.userFilesystems)}`);
        this.sourcesHeap = {};
        this.filesysContainer.replaceChildren();
        this.treeView.replaceChildren();
        this.elementHeap = {};
        for (const key of Object.keys(this.model.userFilesystems)) {
            let fsInfo = this.model.userFilesystems[key];
            this.addFilesystemItem(fsInfo);
        }
    }
    addFilesystemItem(fsInfo) {
        let fsItem = new _FssFilesysItem__WEBPACK_IMPORTED_MODULE_6__.FssFilesysItem(this.model, fsInfo, [this.handleFilesystemClicked.bind(this)]);
        this.sourcesHeap[fsInfo.name] = fsItem;
        fsItem.setMetadata(fsInfo.path);
        this.filesysContainer.appendChild(fsItem.root);
    }
    async handleFilesystemClicked(fsInfo) {
        for (let fsElem of this.filesysContainer.children) {
            // Set clicked FS to selected state (+colorize), deselect others
            if (!(fsElem.dataset.fssname in this.sourcesHeap)) {
                // This should never happen
                _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.error('Error selecting filesystem');
                break;
            }
            let wrapper = this.sourcesHeap[fsElem.dataset.fssname];
            if (fsElem.dataset.fssname == fsInfo.name) {
                wrapper.selected = true;
            }
            else {
                wrapper.selected = false;
            }
        }
        this.model.setActiveFilesystem(fsInfo.name);
        await this.fetchAndDisplayFileInfo(fsInfo.name);
    }
    getNodeForPath(source_path) {
        // Traverse the dir tree and get the node for the supplied path
        let nodeForPath = null;
        // Dir tree nodes store a path relative to the fs root directly on the node (with
        // an absolute path stored elsewhere, in the metadata attribute). Children of nodes
        // are keyed by path segment from their parent (so at the node for a folder "my_data",
        // a child path "my_data/salinity.csv" has a key "salinity.csv" in the node's children
        // leading to that node).
        // 
        // Here, we get the supplied path relative to fs root, then split it into path segments,
        // and start traversing the dir tree using those segments to find the next child node
        // (so if "/my_cool/root_directory" is the fs root, "/my_cool/root_directory/data_files/userfile.dat"
        // will start looking for the "data_files" child node first.
        let relPathFromFsRoot = path__WEBPACK_IMPORTED_MODULE_0__.relative(this.model.getActiveFilesystemInfo().path, source_path);
        // Traverse nodes using the source path's segments
        let currentNode = this.dirTree;
        for (const segment of relPathFromFsRoot.split('/').filter((c) => c.length > 0)) {
            if (segment in currentNode['children']) {
                currentNode = currentNode['children'][segment];
            }
            else {
                break;
            }
        }
        // Check if the desired node was found, set result if so
        if (currentNode.metadata.name == source_path) {
            nodeForPath = currentNode;
        }
        return nodeForPath;
    }
    async lazyLoad(source_path) {
        // Fetch files for a given folder and update the dir tree with the results
        _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.info(`Calling lazy load for ${source_path}`);
        const response = await this.model.listDirectory(this.model.userFilesystems[this.model.activeFilesystem].key, source_path);
        if ((response === null || response === void 0 ? void 0 : response.status) != 'success' || !(response === null || response === void 0 ? void 0 : response.content)) {
            // TODO refactor validation
            _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.error(`Error fetching files for path ${source_path}`); // TODO jupyter info print
            return;
        }
        _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.debug(`Response: (${JSON.stringify(response)})`);
        // Get the dir tree node for this path (updates go into this subtree)
        let nodeForPath = this.getNodeForPath(source_path);
        // Logger.debug(`Found node: ${JSON.stringify(nodeForPath)}`);
        if (!nodeForPath) {
            _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.error(`Error: Bad path for ${source_path}`);
            return;
        }
        if (!nodeForPath.fetch) { // Only fetch if this hasn't been fetched before
            // Update the dir tree/data
            this.updateTree(nodeForPath, response['content'], source_path);
            nodeForPath.fetch = true;
            // Logger.debug(`After fetch: ${JSON.stringify(nodeForPath)}`);
        }
        else {
            // Already fetched this child path, ignore and return
            _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.info('Skipping lazy load, already fetched for ${source_path}');
            return;
        }
        // Update the TreeView in the UI
        await this.updateFileBrowserView(nodeForPath);
        if (nodeForPath.id.toString() in this.elementHeap) {
            let uiElement = this.elementHeap[nodeForPath.id.toString()];
            uiElement.expandItem();
            // Logger.debug(`[FSSpec] StartNode children after lazy load:\n\n${uiElement.root.innerHTML}`);
        }
    }
    getElementForNode(ident) {
        return this.elementHeap[ident.toString()];
    }
    async updateFileBrowserView(startNode = null) {
        // Update/sync the tree view with the file data for this filesys
        _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.info('Updating file browser view');
        let dirTree = this.dirTree;
        let buildTargets = { '/': [this.treeView, dirTree.children] };
        // Set up either a partial update (from a given start node), or
        // a complete tear down and repopulate from scratch (for new data)
        if (startNode) {
            dirTree = startNode;
            let startPath = startNode.path;
            buildTargets = {};
            buildTargets[startPath] = [this.getElementForNode(startNode.id), startNode.children];
        }
        else {
            this.treeView.replaceChildren();
        }
        // Traverse iteratively
        while (Object.keys(buildTargets).length > 0) {
            // Start with root, add children
            let deleteQueue = [];
            for (const absPath of Object.keys(buildTargets)) {
                let elemParent = buildTargets[absPath][0];
                let childPaths = buildTargets[absPath][1];
                if (!childPaths) {
                    // TODO: Create a placeholder child item for this dir
                }
                for (let [pathSegment, pathInfo] of Object.entries(childPaths)) {
                    let item = new _FssTreeItem__WEBPACK_IMPORTED_MODULE_7__.FssTreeItem(this.model, [this.lazyLoad.bind(this)], true, true);
                    item.setMetadata(pathInfo.path, pathInfo.metadata.size);
                    item.setText(pathSegment);
                    // (pathInfo as any).ui = item;
                    elemParent.appendChild(item.root);
                    // Store ID and element in the element heap
                    let item_id = UniqueId.get_id();
                    pathInfo.id = item_id;
                    this.elementHeap[item_id.toString()] = item;
                    if (Object.keys(pathInfo.children).length > 0 ||
                        ('type' in pathInfo.metadata && pathInfo.metadata.type == 'directory')) {
                        item.setType('dir');
                    }
                    else {
                        item.setType('file');
                    }
                    if (Object.keys(pathInfo.children).length > 0) {
                        buildTargets[pathInfo.path] = [item, pathInfo.children];
                    }
                }
                deleteQueue.push(absPath);
            }
            for (const item of deleteQueue) {
                delete buildTargets[item];
            }
        }
    }
    async fetchAndDisplayFileInfo(fsname) {
        // Fetch files for this filesystem
        const response = await this.model.listDirectory(this.model.userFilesystems[this.model.activeFilesystem].key);
        if (!('status' in response) || !(response.status == 'success') || !('content' in response)) {
            // TODO refactor validation
            _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.error(`Error fetching files for filesystem ${fsname}`); // TODO jupyter info print
            return;
        }
        const pathInfos = response['content'].sort((a, b) => { return a.name.localeCompare(b.name); });
        // Update current filesystem display labels
        this.selectedFsLabel.innerText = `${fsname}`;
        // Build a directory tree and update the display
        this.dirTree = this.buildTree(pathInfos, this.model.userFilesystems[fsname].path);
        this.updateFileBrowserView();
    }
    updateTree(tree, pathInfoList, rootPath) {
        // Update a given tree or subtree by building/populating
        // a nested tree structure based on the provided pathInfos
        let dirTree = tree;
        for (let pdata of pathInfoList) {
            let name = path__WEBPACK_IMPORTED_MODULE_0__.relative(rootPath, pdata.name);
            // TODO: path sep normalization
            // Go segment by segment, building the nested path tree
            let segments = name.split('/').filter((c) => c.length > 0);
            let parentLocation = dirTree['children'];
            for (let i = 0; i < segments.length; i++) {
                // Get path components and a key for this subpath
                let subpath = [];
                for (let j = 0; j <= i; j++) {
                    subpath.push(segments[j]);
                }
                let segment = segments[i];
                if (segment in parentLocation) {
                    parentLocation = parentLocation[segment]['children'];
                }
                else {
                    let children = {};
                    let metadata = {};
                    if (i == Math.max(0, segments.length - 1)) {
                        metadata = pdata;
                    }
                    parentLocation[segment] = {
                        'path': pdata.name,
                        'children': children,
                        'metadata': metadata,
                        'fetch': false,
                        'id': null,
                    };
                    parentLocation = parentLocation[segment]['children'];
                }
            }
        }
        return dirTree;
    }
    clearFileData() {
        this.dirTree = {};
        this.elementHeap = {};
    }
    buildTree(pathInfoList, rootPath) {
        // Start building a new directory tree structure from scratch,
        // update/populate it using a list of pathInfos ([path + metadata] items)
        this.clearFileData();
        let dirTree = {
            'path': '/',
            'children': {},
            'fetch': true,
            'metadata': { path: rootPath },
            'id': null,
        };
        this.updateTree(dirTree, pathInfoList, rootPath);
        return dirTree;
    }
}
/**
 * Initialization data for the jupyterFsspec extension.
 */
const plugin = {
    id: 'jupyterFsspec:plugin',
    description: 'A Jupyter interface for fsspec.',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: async (app, palette, settingRegistry) => {
        console.log('JupyterLab extension jupyterFsspec is activated!');
        _logger__WEBPACK_IMPORTED_MODULE_5__.Logger.setLevel(_logger__WEBPACK_IMPORTED_MODULE_5__.Logger.DEBUG);
        // Auto initialize the model
        let fsspecModel = new _handler_fileOperations__WEBPACK_IMPORTED_MODULE_8__.FsspecModel();
        await fsspecModel.initialize();
        // Use the model to initialize the widget and add to the UI
        let fsspec_widget = new FsspecWidget(fsspecModel);
        fsspec_widget.id = 'jupyterFsspec:widget';
        app.shell.add(fsspec_widget, 'right');
        // // TODO finish this
        // if (settingRegistry) {
        //   settingRegistry
        //     .load(plugin.id)
        //     .then(settings => {
        //       Logger.info(`[FSSpec] Settings loaded: ${settings.composite}`);
        //     })
        //     .catch(reason => {
        //       Logger.error(`[FSSpec] Failed to load settings for jupyterFsspec: ${reason}`);
        //     });
        // }
        const { commands } = app;
        const commandToolkit = 'jupyter_fsspec:open-toolkit';
        commands.addCommand(commandToolkit, {
            label: 'Open fsspec Toolkit Widget',
            execute: () => {
                const widget = new _FileManager__WEBPACK_IMPORTED_MODULE_9__.FileManagerWidget();
                widget.id = 'jupyter_fsspec-toolkit-widget';
                widget.title.label = 'fsspec Toolkit Widget';
                app.shell.add(widget, 'right');
            }
        });
        palette.addItem({
            command: commandToolkit,
            category: 'My Extensions',
            args: { origin: 'from palette ' }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/logger.js":
/*!***********************!*\
  !*** ./lib/logger.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Logger: () => (/* binding */ Logger)
/* harmony export */ });
// A simple toggleable (on/off) logger with levels for debugging
class Logger {
    static print(message, log_level) {
        if (log_level && log_level <= Logger.level) {
            console.log(message);
        }
    }
    static debug(message) {
        Logger.print(message, Logger.DEBUG);
    }
    static info(message) {
        Logger.print(message, Logger.INFO);
    }
    static warn(message) {
        Logger.print(message, Logger.WARN);
    }
    static error(message) {
        Logger.print(message, Logger.ERROR);
    }
    static setLevel(value) {
        Logger.level = value;
    }
}
Logger.NONE = 0;
Logger.ERROR = 1;
Logger.WARN = 2;
Logger.INFO = 3;
Logger.DEBUG = 4;
Logger.level = Logger.INFO;



/***/ }),

/***/ "./lib/treeContext.js":
/*!****************************!*\
  !*** ./lib/treeContext.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FssContextMenu: () => (/* binding */ FssContextMenu)
/* harmony export */ });
// Right-click/context menu for file items
class FssContextMenu {
    constructor(model) {
        this.clicked = false;
        let root = document.createElement('div');
        root.classList.add('jfss-tree-context-menu');
        this.root = root;
        this.model = model;
        let menuItem = document.createElement('div');
        menuItem.classList.add('jfss-tree-context-item');
        menuItem.innerText = 'Copy Path';
        menuItem.addEventListener('mouseenter', this.handleItemHover.bind(this));
        menuItem.addEventListener('mouseleave', this.handleItemUnhover.bind(this));
        menuItem.addEventListener('click', this.handleItemClick.bind(this));
        menuItem.dataset.fssContextType = 'copyPath';
        root.appendChild(menuItem);
        root.addEventListener('mouseleave', this.handleMouseExit.bind(this), false);
    }
    handleItemClick(event) {
        if (event.target.dataset.fssContextType == 'copyPath') {
            let info = this.model.getActiveFilesystemInfo();
            let protocol = info === null || info === void 0 ? void 0 : info.canonical_path.slice(0, info.canonical_path.length - info.path.length);
            if (protocol) {
                let canonical = protocol + '/' + this.root.dataset.fss.replace(/^\/+/, () => '');
                navigator.clipboard.writeText(canonical).then(() => {
                    console.log('Copy path: ' + canonical);
                    this.root.remove();
                }, () => {
                    console.log('Copy path failed: ' + canonical);
                    this.root.remove();
                });
            }
        }
    }
    handleItemHover(event) {
        event.target.style.backgroundColor = 'var(--jp-layout-color2)';
    }
    handleItemUnhover(event) {
        event.target.style.backgroundColor = 'var(--jp-layout-color1)';
    }
    handleMouseExit(event) {
        event.preventDefault();
        this.root.remove();
        return false;
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.e8e8ca2015c35949d3cb.js.map