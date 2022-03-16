var socket = io.connect('http://' + document.domain + ':' + location.port);

var browsedType = "Classes";
var classTree;
var itemNamespacePath = [];
var currentItemKey = "__classes__"

function updateClassList(treeRoot, isAbsoluteRoot) {
    currentItemKey = "__classes__";
    updateItemList(treeRoot, isAbsoluteRoot, currentItemKey);
}

function updateEnumList(treeRoot, isAbsoluteRoot) {
    currentItemKey = "__enums__";
    updateItemList(treeRoot, isAbsoluteRoot, currentItemKey);
}

function updateFunctionList(treeRoot, isAbsoluteRoot) {
    currentItemKey = "__functions__";
    updateItemList(treeRoot, isAbsoluteRoot, currentItemKey);
}

function updateFileList(treeRoot, isAbsoluteRoot) {
    currentItemKey = "__files__";
    updateItemList(treeRoot, isAbsoluteRoot, currentItemKey);
}

function updateItemList(treeRoot, isAbsoluteRoot, childKey) {
    const itemList = document.getElementById('ItemList');
    itemList.innerHTML = ""
    if(!isAbsoluteRoot){
        itemHTML = "<li class=\"vertical-navbar control-item\" ><a href=\"#\" onclick=\"browseNamespaceBack();return false;\">Back</a></li>";
        itemList.insertAdjacentHTML('beforeend', itemHTML);
    }
    for (key of Object.keys(treeRoot).sort().values()) {
        var itemHTML = "";
        if (key != childKey)
        {
            itemHTML = "<li class=\"vertical-navbar namespace-item\" ><a href=\"#\" onclick=\"browseNamespace('"+key+"');return false;\">"+key+"</a></li>";
            itemList.insertAdjacentHTML('beforeend', itemHTML);
        }
    }
    if (childKey in treeRoot) {
        for (item of treeRoot[childKey].sort().values()){
            name = item;
            classPath = item;
            if (childKey != "__functions__" && itemNamespacePath.length > 0)
            {
                classPath = itemNamespacePath.join("::")+'::'+item
            }
            targetFunc = "requestClassData"
            if(childKey == "__enums__") {
                targetFunc = "requestEnumData"
            } else if(childKey == "__functions__") {
                targetFunc = "requestFunctionData"
                classPath = item["fullDef"];
                name = item["name"];
            } else if(childKey == "__files__") {
                targetFunc = "requestFileData"
            }
            itemHTML = "<li class=\"vertical-navbar class-item\" ><a href=\"#\" onclick=\""+targetFunc+"('"+classPath+"');return false;\">"+name+"</a></li>";
            itemList.insertAdjacentHTML('beforeend', itemHTML);
        }
    }
}

function browseCurrentNamespacePath() {
    tree = classTree;
    for (name of itemNamespacePath.values()) {
        tree = tree[name];
    }
    updateItemList(tree, itemNamespacePath.length == 0, currentItemKey);

}

function browseNamespace(namespace) {
    tree = classTree;
    for (name of itemNamespacePath.values()) {
        tree = tree[name];
    }
    if (namespace in tree) {
        itemNamespacePath.push(namespace)
        browseCurrentNamespacePath();
    }
}

function browseNamespaceBack() {
    if (itemNamespacePath.length == 0)
    {
        return;
    }
    itemNamespacePath.pop()
    browseCurrentNamespacePath();
}

function updateClassView(klass, diag) {
    const itemName = document.getElementById('ItemName');
    const itemDiag = document.getElementById('ItemDiag');
    const itemDesc = document.getElementById('ItemDesc');

    itemName.innerHTML = klass["name"];
    console.log(diag)
    itemDiag.innerHTML = diag;
    namespace = klass["namespace"];
    if (namespace.length == 0){
        namespace = "None";
    }
    desc = "<b>Name : </b>"+klass["name"]+"<br>"+
           "<b>Namespace : </b>"+namespace+"<br>"+
           "<b>File : </b><a href=\"#\" onclick=\"requestFileData('"+klass["file"]+"');return false;\">"+klass["file"]+"</a><br>";

    if (klass["parents"].length > 0) {
        desc += "<b>Inherits from : </b><br><ul class=\"inherits-link\">";
        for (parent of klass["parents"]) {
            desc += "<li class=\"inherits-link\"><a href=\"#\" onclick=\"requestClassData('"+parent+"');return false;\">"+parent+"</a></li>"
        }
        desc += "</ul><br>";
    }
    itemDesc.innerHTML = desc;
    itemDiag.removeAttribute('data-processed');
    let insert = function (code) {
      itemDiag.innerHTML = code;
    };
    mermaid.render("preparedScheme", diag, insert);
    var svg = document.getElementById("preparedScheme");
    var links = svg.getElementsByTagName("a")
    for (var i = 0; i < links.length; i++) {
        let hint = links[i].getAttribute('xlink:href')
        links[i].removeAttribute('xlink:href');
        links[i].setAttribute("href","#");
        links[i].setAttribute("onclick", "onNodeClick('"+hint+"');");
    }

}

function updateEnumView(enumData, diag) {
    const itemName = document.getElementById('ItemName');
    const itemDiag = document.getElementById('ItemDiag');
    const itemDesc = document.getElementById('ItemDesc');

    itemName.innerHTML = enumData["name"];
    console.log(diag)
    itemDiag.innerHTML = diag;
    namespace = enumData["namespace"];
    if (namespace.length == 0){
        namespace = "None";
    }
    desc = "<b>Name : </b>"+enumData["name"]+"<br>"+
           "<b>Namespace : </b>"+namespace+"<br>"+
           "<b>File : </b><a href=\"#\" onclick=\"requestFileData('"+enumData["file"]+"');return false;\">"+enumData["file"]+"</a><br>";
    itemDesc.innerHTML = desc;
    itemDiag.removeAttribute('data-processed');
    let insert = function (code) {
      itemDiag.innerHTML = code;
    };
    mermaid.render("preparedScheme", diag, insert);
}

function updateFunctionView(functionData) {
    const itemName = document.getElementById('ItemName');
    const itemDiag = document.getElementById('ItemDiag');
    const itemDesc = document.getElementById('ItemDesc');

    itemName.innerHTML = functionData["name"];
    itemDiag.innerHTML = "";
    namespace = functionData["namespace"];
    if (namespace.length == 0){
        namespace = "None";
    }
    defLine = functionData["rtype"]+" "+functionData["name"]+"("
    for (key of Object.keys(functionData["params"]).values()) {
        defLine += functionData["params"][key]+" "+key+", "
    }
    defLine = defLine.slice(0, -2);
    defLine += ")";
    defLine = functionData["doxygen"]+"\n"+defLine;
    desc = "<b>Name : </b>"+functionData["name"]+"<br>"+
           "<b>Namespace : </b>"+namespace+"<br>"+
           "<b>File : </b><a href=\"#\" onclick=\"requestFileData('"+functionData["file"]+"');return false;\">"+functionData["file"]+"</a><br>"+
           "<h2>Definition</h2>"+
           "<div class=\"left\"><pre><code>"+defLine+"</code></pre></div>";
    itemDesc.innerHTML = desc;
    hljs.highlightAll();
}

function updateFileView(fileData) {
    const itemName = document.getElementById('ItemName');
    const itemDiag = document.getElementById('ItemDiag');
    const itemDesc = document.getElementById('ItemDesc');

    itemName.innerHTML = fileData["name"];
    itemDiag.innerHTML = "";
    path = fileData["path"];

    refStr = "";
    if ("classes" in fileData["objects"] && fileData["objects"]["classes"].length > 0) {
        refStr += "<h3>Classes<h3><ul class=\"nobullets\">"
        for (value of fileData["objects"]["classes"]) {
            refStr += "<li><a href=\"#\" onclick=\"requestClassData('"+value+"');return false;\">"+value+"</a></li>"
        }
        refStr += "</ul>"
    }
    if ("enums" in fileData["objects"] && fileData["objects"]["enums"].length > 0) {
        refStr += "<h3>Enums<h3><ul class=\"nobullets\">"
        for (value of fileData["objects"]["enums"]) {
            refStr += "<li><a href=\"#\" onclick=\"requestEnumData('"+value+"');return false;\">"+value+"</a></li>"
        }
        refStr += "</ul>"
    }
    if ("functions" in fileData["objects"] && fileData["objects"]["functions"].length > 0) {
        refStr += "<h3>Functions<h3><ul class=\"nobullets\">"
        for (value of fileData["objects"]["functions"]) {
            refStr += "<li><a href=\"#\" onclick=\"requestFunctionData('"+value+"');return false;\">"+value+"</a></li>"
        }
        refStr += "</ul>"
    }

    desc = "<b>Name : </b>"+fileData["name"]+"<br>"+
           "<b>Path : </b>"+path+"<br>"+
           "<h2>References</h2><br>" +
           refStr+
           "<h2>Content</h2><br>" +
           "<div class=\"left\"><pre><code>"+fileData["content"]+"</code></pre></div>";
    itemDesc.innerHTML = desc;
    hljs.highlightAll();
}

function requestClassData(klass) {
    console.log("requestClassData : "+klass)
    socket.emit('fetchClassData', {
        data: 'request fetchClassData',
        className : klass
    });
}

function requestEnumData(enumData) {
    console.log("requestEnumData : "+enumData)
    socket.emit('fetchEnumData', {
        data: 'request fetchEnumData',
        enumName : enumData
    });
}

function requestFunctionData(functionData) {
    console.log("requestFunctionData : "+functionData)
    socket.emit('fetchFunctionData', {
        data: 'request fetchFunctionData',
        functionDef : functionData
    });
}

function requestFileData(fileData) {
    console.log("requestFileData : "+fileData)
    socket.emit('fetchFileData', {
        data: 'request fetchFileData',
        fileName : fileData
    });
}

function setupSearch() {
    const itemName = document.getElementById('ItemName');
    const itemDiag = document.getElementById('ItemDiag');
    const itemDesc = document.getElementById('ItemDesc');

    itemName.innerHTML = "Search";
    itemDesc.innerHTML = "<input type=\"search\" id=\"code-search-text\" name=\"q\"><button onclick=\"performSearch();\">Search</button>";
    itemDiag.innerHTML = "";
}

function performSearch() {
    const itemSearch = document.getElementById('code-search-text');
    token = itemSearch.value
    socket.emit('searchData', {
        data: 'request searchData',
        token : token
    });
}

function showSearchResult(res) {
    const itemDiag = document.getElementById('ItemDiag');
    presentation = "Found "+res.length+" results.<h2>Results :</h2><div class=\"left\">";
    for (item of res) {
        path = item[0];
        context = item[1];
        presentation += "<div><a href=\"#\" onclick=\"requestFileData('"+path+"');return false;\">"+path+"</a></div><br><div><pre><code>"+context+"</pre></code></div><br><br>";
    }
    presentation += "</div>"
    itemDiag.innerHTML = presentation;
    hljs.highlightAll();
}

socket.on( 'connect', function() {
    pathItems = window.location.pathname.split("/")
    key = pathItems[pathItems.length - 1];
    console.log("fetch  : "+key)
    if (key == "classes") {
        currentItemKey = "__classes__";
        socket.emit('fetchAnalysedClassNames', {
            data: 'request data to feed browse'
        });
    } else if (key == "enums") {
        currentItemKey = "__enums__";
        socket.emit('fetchAnalysedEnumNames', {
            data: 'request data to feed browse'
        });
    } else if (key == "functions") {
        currentItemKey = "__functions__";
        socket.emit('fetchAnalysedFunctionNames', {
            data: 'request data to feed browse'
        });
    } else if (key == "files" || key == 'search') {
        currentItemKey = "__files__";
        socket.emit('fetchAnalysedFileNames', {
            data: 'request data to feed browse'
        });
        if(key == 'search')
            setupSearch()
    } else {
        console.log("Unknow path to handle : "+key+" in "+window.location.pathname)
    }
})

socket.on( 'classeNamesChange', function( msg ) {
    console.log("classeNamesChange received");
    classTree = msg.tree;
    updateClassList(classTree, true);
})

socket.on( 'enumNamesChange', function( msg ) {
    console.log("enumNamesChange received");
    classTree = msg.tree;
    updateEnumList(classTree, true);
})

socket.on( 'functionNamesChange', function( msg ) {
    console.log("functionNamesChange received");
    classTree = msg.tree;
    updateFunctionList(classTree, true);
})

socket.on( 'fileNamesChange', function( msg ) {
    console.log("fileNamesChange received");
    classTree = msg.tree;
    updateFileList(classTree, true);
})

socket.on( 'classDataChange', function( msg ) {
    console.log("classDataChange received");
    klass = msg.class;
    diag = msg.mermaidDiag;
    updateClassView(klass, diag);
})

socket.on( 'enumDataChange', function( msg ) {
    console.log("enumDataChange received");
    enumData = msg.enum;
    diag = msg.mermaidDiag;
    updateEnumView(enumData, diag);
})

socket.on( 'functionDataChange', function( msg ) {
    console.log("functionDataChange received");
    functionData = msg.function;
    updateFunctionView(functionData);
})

socket.on( 'fileDataChange', function( msg ) {
    console.log("fileDataChange received");
    fileData = msg.file;
    updateFileView(fileData);
})

socket.on( 'searchResult', function( msg ) {
    console.log("searchResult received");
    res = msg.res;
    showSearchResult(res);
})

var onNodeClick = function(text){
    items = text.split("££")
    if(items[0] == "class")
        requestClassData(items[1]);
    else if(items[0] == "enum")
        requestEnumData(items[1]);
}
var config = {
    startOnLoad:true,
    securityLevel:'loose',
};
mermaid.initialize(config);

hljs.configure({languages: ["c","cpp","python","java","kotlin"]})
