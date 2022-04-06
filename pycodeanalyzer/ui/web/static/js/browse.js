/* global io, mermaid, hljs */

const socket = io.connect('http://' + document.domain + ':' + location.port);

let classTree;
const itemNamespacePath = [];
let currentItemKey = '__classes__';

function updateClassList(treeRoot, isAbsoluteRoot) {
	currentItemKey = '__classes__';
	updateItemList(treeRoot, isAbsoluteRoot, currentItemKey);
}

function updateEnumList(treeRoot, isAbsoluteRoot) {
	currentItemKey = '__enums__';
	updateItemList(treeRoot, isAbsoluteRoot, currentItemKey);
}

function updateFunctionList(treeRoot, isAbsoluteRoot) {
	currentItemKey = '__functions__';
	updateItemList(treeRoot, isAbsoluteRoot, currentItemKey);
}

function updateFileList(treeRoot, isAbsoluteRoot) {
	currentItemKey = '__files__';
	updateItemList(treeRoot, isAbsoluteRoot, currentItemKey);
}

function updateItemList(treeRoot, isAbsoluteRoot, childKey) {
	const itemList = document.getElementById('ItemList');
	let itemHTML = '';
	itemList.innerHTML = '';
	if (!isAbsoluteRoot) {
		itemHTML = '<li class="vertical-navbar control-item" ><a href="#" onclick="browseNamespaceBack();return false;">Back</a></li>';
		itemList.insertAdjacentHTML('beforeend', itemHTML);
	}

	for (const key of Object.keys(treeRoot).sort().values()) {
		itemHTML = '';
		if (key !== childKey) {
			itemHTML = '<li class="vertical-navbar namespace-item" ><a href="#" onclick="browseNamespace(\'' + key + '\');return false;">' + key + '</a></li>';
			itemList.insertAdjacentHTML('beforeend', itemHTML);
		}
	}

	if (childKey in treeRoot) {
		for (const item of treeRoot[childKey].sort().values()) {
			let name = item;
			let classPath = item;
			if (childKey !== '__functions__' && itemNamespacePath.length > 0) {
				classPath = itemNamespacePath.join('::') + '::' + item;
			}

			let targetFunc = 'requestClassData';
			if (childKey === '__enums__') {
				targetFunc = 'requestEnumData';
			} else if (childKey === '__functions__') {
				targetFunc = 'requestFunctionData';
				classPath = item.fullDef;
				name = item.name;
			} else if (childKey === '__files__') {
				targetFunc = 'requestFileData';
			}

			itemHTML = '<li class="vertical-navbar class-item" ><a href="#" onclick="' + targetFunc + '(\'' + classPath + '\');return false;">' + name + '</a></li>';
			itemList.insertAdjacentHTML('beforeend', itemHTML);
		}
	}
}

function browseCurrentNamespacePath() {
	let tree = classTree;
	for (const name of itemNamespacePath.values()) {
		tree = tree[name];
	}

	updateItemList(tree, itemNamespacePath.length === 0, currentItemKey);
}

// eslint-disable-next-line no-unused-vars
function browseNamespace(namespace) {
	let tree = classTree;
	for (const name of itemNamespacePath.values()) {
		tree = tree[name];
	}

	if (namespace in tree) {
		itemNamespacePath.push(namespace);
		browseCurrentNamespacePath();
	}
}

// eslint-disable-next-line no-unused-vars
function browseNamespaceBack() {
	if (itemNamespacePath.length === 0) {
		return;
	}

	itemNamespacePath.pop();
	browseCurrentNamespacePath();
}

function updateClassView(klass, diag) {
	const itemName = document.getElementById('ItemName');
	const itemDiag = document.getElementById('ItemDiag');
	const itemDesc = document.getElementById('ItemDesc');
	const itemUsedBy = document.getElementById('ItemUsedBy');

	itemName.innerHTML = klass.name;
	console.log(diag);
	itemDiag.innerHTML = diag;
	// eslint-disable-next-line prefer-destructuring
	let namespace = klass.namespace;
	if (namespace.length === 0) {
		namespace = 'None';
	}

	let desc = '<b>Name : </b>' + klass.name + '<br>'
           + '<b>Namespace : </b>' + namespace + '<br>'
           + '<b>File : </b><a href="#" onclick="requestFileData(\'' + klass.file + '\');return false;">' + klass.file + '</a><br>';

	if (klass.parents.length > 0) {
		desc += '<b>Inherits from : </b><br><ul class="inherits-link">';
		for (const parent of klass.parents) {
			if (parent.startsWith('$_EXTERNAL_$')) {
				desc += '<li class="inherits-link">' + parent.replace('$_EXTERNAL_$', '') + '</li>';
			} else {
				desc += '<li class="inherits-link"><a href="#" onclick="requestClassData(\'' + parent + '\');return false;">' + parent + '</a></li>';
			}
		}

		desc += '</ul><br>';
	}

	itemDesc.innerHTML = desc;
	itemDiag.removeAttribute('data-processed');
	const insert = function (code) {
		itemDiag.innerHTML = code;
	};

	let usedByList = '<h3>Used by</h3>';
	usedByList += '<h4>Classes</h4><ul class="inherits-link">';
	if (klass.usedBy.Classes.length > 0) {
		for (const userItem of klass.usedBy.Classes) {
			usedByList += '<li class="inherits-link"><a href="#" onclick="requestClassData(\'' + userItem + '\');return false;">' + userItem + '</a></li>';
		}
	} else {
		usedByList += '<li class="inherits-link">None</li>';
	}

	usedByList += '</ul>';
	itemUsedBy.innerHTML = usedByList;

	mermaid.render('preparedScheme', diag, insert);
	const svg = document.getElementById('preparedScheme');
	const links = svg.getElementsByTagName('a');
	for (let i = 0; i < links.length; i++) {
		const hint = links[i].getAttribute('xlink:href');
		links[i].removeAttribute('xlink:href');
		links[i].setAttribute('href', '#');
		links[i].setAttribute('onclick', 'onNodeClick(\'' + hint + '\');');
	}
}

function updateEnumView(enumData, diag) {
	const itemName = document.getElementById('ItemName');
	const itemDiag = document.getElementById('ItemDiag');
	const itemDesc = document.getElementById('ItemDesc');
	const itemUsedBy = document.getElementById('ItemUsedBy');

	itemName.innerHTML = enumData.name;
	console.log(diag);
	itemDiag.innerHTML = diag;
	// eslint-disable-next-line prefer-destructuring
	let namespace = enumData.namespace;
	if (namespace.length === 0) {
		namespace = 'None';
	}

	const desc = '<b>Name : </b>' + enumData.name + '<br>'
           + '<b>Namespace : </b>' + namespace + '<br>'
           + '<b>File : </b><a href="#" onclick="requestFileData(\'' + enumData.file + '\');return false;">' + enumData.file + '</a><br>';
	itemDesc.innerHTML = desc;
	itemDiag.removeAttribute('data-processed');
	const insert = function (code) {
		itemDiag.innerHTML = code;
	};

	let usedByList = '<h3>Used by</h3>';
	usedByList += '<h4>Classes</h4><ul class="inherits-link">';
	if (enumData.usedBy.Classes.length > 0) {
		for (const userItem of enumData.usedBy.Classes) {
			usedByList += '<li class="inherits-link"><a href="#" onclick="requestClassData(\'' + userItem + '\');return false;">' + userItem + '</a></li>';
		}
	} else {
		usedByList += '<li class="inherits-link">None</li>';
	}

	usedByList += '</ul>';
	itemUsedBy.innerHTML = usedByList;

	mermaid.render('preparedScheme', diag, insert);
}

function updateFunctionView(functionData) {
	const itemName = document.getElementById('ItemName');
	const itemDiag = document.getElementById('ItemDiag');
	const itemDesc = document.getElementById('ItemDesc');

	itemName.innerHTML = functionData.name;
	itemDiag.innerHTML = '';
	// eslint-disable-next-line prefer-destructuring
	let namespace = functionData.namespace;
	if (namespace.length === 0) {
		namespace = 'None';
	}

	let defLine = functionData.rtype + ' ' + functionData.name + '(';

	if (functionData.params.length > 0) {
		for (const key of Object.keys(functionData.params).values()) {
			defLine += functionData.params[key] + ' ' + key + ', ';
		}

		defLine = defLine.slice(0, -2);
	}

	defLine += ')';
	defLine = functionData.doxygen + '\n' + defLine;
	const desc = '<b>Name : </b>' + functionData.name + '<br>'
           + '<b>Namespace : </b>' + namespace + '<br>'
           + '<b>File : </b><a href="#" onclick="requestFileData(\'' + functionData.file + '\');return false;">' + functionData.file + '</a><br>'
           + '<h2>Definition</h2>'
           + '<div class="left"><pre><code>' + defLine + '</code></pre></div>';
	itemDesc.innerHTML = desc;
	hljs.highlightAll();
}

function updateFileView(fileData) {
	const itemName = document.getElementById('ItemName');
	const itemDiag = document.getElementById('ItemDiag');
	const itemDesc = document.getElementById('ItemDesc');
	const {path} = fileData;

	itemName.innerHTML = fileData.name;
	itemDiag.innerHTML = '';

	let refStr = '';
	if ('classes' in fileData.objects && fileData.objects.classes.length > 0) {
		refStr += '<h3>Classes<h3><ul class="nobullets">';
		for (const value of fileData.objects.classes) {
			refStr += '<li><a href="#" onclick="requestClassData(\'' + value + '\');return false;">' + value + '</a></li>';
		}

		refStr += '</ul>';
	}

	if ('enums' in fileData.objects && fileData.objects.enums.length > 0) {
		refStr += '<h3>Enums<h3><ul class="nobullets">';
		for (const value of fileData.objects.enums) {
			refStr += '<li><a href="#" onclick="requestEnumData(\'' + value + '\');return false;">' + value + '</a></li>';
		}

		refStr += '</ul>';
	}

	if ('functions' in fileData.objects && fileData.objects.functions.length > 0) {
		refStr += '<h3>Functions<h3><ul class="nobullets">';
		for (const value of fileData.objects.functions) {
			refStr += '<li><a href="#" onclick="requestFunctionData(\'' + value + '\');return false;">' + value + '</a></li>';
		}

		refStr += '</ul>';
	}

	const desc = '<b>Name : </b>' + fileData.name + '<br>'
           + '<b>Path : </b>' + path + '<br>'
           + '<h2>References</h2><br>'
           + refStr
           + '<h2>Content</h2><br>'
           + '<div class="left"><pre><code>' + fileData.content + '</code></pre></div>';
	itemDesc.innerHTML = desc;
	hljs.highlightAll();
}

function requestClassData(klass) {
	console.log('requestClassData : ' + klass);
	socket.emit('fetchClassData', {
		data: 'request fetchClassData',
		className: klass,
	});
}

function requestEnumData(enumData) {
	console.log('requestEnumData : ' + enumData);
	socket.emit('fetchEnumData', {
		data: 'request fetchEnumData',
		enumName: enumData,
	});
}

// eslint-disable-next-line no-unused-vars
function requestFunctionData(functionData) {
	console.log('requestFunctionData : ' + functionData);
	socket.emit('fetchFunctionData', {
		data: 'request fetchFunctionData',
		functionDef: functionData,
	});
}

// eslint-disable-next-line no-unused-vars
function requestFileData(fileData) {
	console.log('requestFileData : ' + fileData);
	socket.emit('fetchFileData', {
		data: 'request fetchFileData',
		fileName: fileData,
	});
}

function setupSearch() {
	const itemName = document.getElementById('ItemName');
	const itemDiag = document.getElementById('ItemDiag');
	const itemDesc = document.getElementById('ItemDesc');

	itemName.innerHTML = 'Search';
	itemDesc.innerHTML = '<input type="search" id="code-search-text" name="q"><button onclick="performSearch();">Search</button>';
	itemDiag.innerHTML = '';
}

// eslint-disable-next-line no-unused-vars
function performSearch() {
	const itemSearch = document.getElementById('code-search-text');
	const token = itemSearch.value;
	socket.emit('searchData', {
		data: 'request searchData',
		token,
	});
}

function showSearchResult(res) {
	const itemDiag = document.getElementById('ItemDiag');
	let presentation = 'Found ' + res.length + ' results.<h2>Results :</h2><div class="left">';
	for (const item of res) {
		const path = item[0];
		const context = item[1];
		presentation += '<div><a href="#" onclick="requestFileData(\'' + path + '\');return false;">' + path + '</a></div><br><div><pre><code>' + context + '</pre></code></div><br><br>';
	}

	presentation += '</div>';
	itemDiag.innerHTML = presentation;
	hljs.highlightAll();
}

socket.on('connect', () => {
	const pathItems = window.location.pathname.split('/');
	const key = pathItems[pathItems.length - 1];
	console.log('fetch  : ' + key);
	if (key === 'classes') {
		currentItemKey = '__classes__';
		socket.emit('fetchAnalysedClassNames', {
			data: 'request data to feed browse',
		});
	} else if (key === 'enums') {
		currentItemKey = '__enums__';
		socket.emit('fetchAnalysedEnumNames', {
			data: 'request data to feed browse',
		});
	} else if (key === 'functions') {
		currentItemKey = '__functions__';
		socket.emit('fetchAnalysedFunctionNames', {
			data: 'request data to feed browse',
		});
	} else if (key === 'files' || key === 'search') {
		currentItemKey = '__files__';
		socket.emit('fetchAnalysedFileNames', {
			data: 'request data to feed browse',
		});
		if (key === 'search') {
			setupSearch();
		}
	} else {
		console.log('Unknow path to handle : ' + key + ' in ' + window.location.pathname);
	}
});

socket.on('classeNamesChange', msg => {
	console.log('classeNamesChange received');
	classTree = msg.tree;
	updateClassList(classTree, true);
});

socket.on('enumNamesChange', msg => {
	console.log('enumNamesChange received');
	classTree = msg.tree;
	updateEnumList(classTree, true);
});

socket.on('functionNamesChange', msg => {
	console.log('functionNamesChange received');
	classTree = msg.tree;
	updateFunctionList(classTree, true);
});

socket.on('fileNamesChange', msg => {
	console.log('fileNamesChange received');
	classTree = msg.tree;
	updateFileList(classTree, true);
});

socket.on('classDataChange', msg => {
	console.log('classDataChange received');
	const klass = msg.class;
	const diag = msg.mermaidDiag;
	updateClassView(klass, diag);
});

socket.on('enumDataChange', msg => {
	console.log('enumDataChange received');
	const enumData = msg.enum;
	const diag = msg.mermaidDiag;
	updateEnumView(enumData, diag);
});

socket.on('functionDataChange', msg => {
	console.log('functionDataChange received');
	const functionData = msg.function;
	updateFunctionView(functionData);
});

socket.on('fileDataChange', msg => {
	console.log('fileDataChange received');
	const fileData = msg.file;
	updateFileView(fileData);
});

socket.on('searchResult', msg => {
	console.log('searchResult received');
	const {res} = msg;
	showSearchResult(res);
});

// eslint-disable-next-line no-unused-vars
function onNodeClick(text) {
	const items = text.split('££');
	if (items[0] === 'class') {
		requestClassData(items[1]);
	} else if (items[0] === 'enum') {
		requestEnumData(items[1]);
	}
}

const config = {
	startOnLoad: true,
	securityLevel: 'loose',
};
mermaid.initialize(config);

hljs.configure({languages: ['c', 'cpp', 'python', 'java', 'kotlin']});
