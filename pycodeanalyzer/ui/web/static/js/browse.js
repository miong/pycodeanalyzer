var socket = io.connect('http://' + document.domain + ':' + location.port);

var browsedType = "Classes";
var classTree;
var classNamespacePath = [];

function updateClassList(treeRoot, isAbsoluteRoot) {
    const itemList = document.getElementById('ItemList');
    itemList.innerHTML = ""
    if(!isAbsoluteRoot){
        itemHTML = "<li class=\"vertical-navbar control-item\" ><a href=\"#\" onclick=\"browseNamespaceBack();return false;\">Back</a></li>";
        itemList.insertAdjacentHTML('beforeend', itemHTML);
    }
    for (key of Object.keys(treeRoot).sort().values()) {
        var itemHTML = "";
        if (key != "__classes__")
        {
            itemHTML = "<li class=\"vertical-navbar namespace-item\" ><a href=\"#\" onclick=\"browseNamespace('"+key+"');return false;\">"+key+"</a></li>";
            itemList.insertAdjacentHTML('beforeend', itemHTML);
        }
    }
    if ("__classes__" in treeRoot) {
        for (klass of treeRoot["__classes__"].sort().values()){
            classPath = klass
            if (classNamespacePath.length > 0)
            {
                classPath = classNamespacePath.join("::")+'::'+klass
            }
            itemHTML = "<li class=\"vertical-navbar class-item\" ><a href=\"#\" onclick=\"requestClassData('"+classPath+"');return false;\">"+klass+"</a></li>";
            itemList.insertAdjacentHTML('beforeend', itemHTML);
        }
    }
}

function browseCurrentNamespacePath() {
    tree = classTree;
    for (name of classNamespacePath.values()) {
        tree = tree[name];
    }
    updateClassList(tree, classNamespacePath.length == 0);

}

function browseNamespace(namespace) {
    tree = classTree;
    for (name of classNamespacePath.values()) {
        tree = tree[name];
    }
    if (namespace in tree) {
        classNamespacePath.push(namespace)
        browseCurrentNamespacePath();
    }
}

function browseNamespaceBack() {
    if (classNamespacePath.length == 0)
    {
        return;
    }
    classNamespacePath.pop()
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
           "<b>File : </b>"+klass["file"]+"<br>";

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
}

function requestClassData(klass) {
    socket.emit('fetchClassData', {
        data: 'request fetchClassData',
        className : klass
    });
}

socket.on( 'connect', function() {
    socket.emit('fetchAnalysedClassNames', {
        data: 'request fetchAnalysedObjectNames'
    });
})

socket.on( 'classeNamesChange', function( msg ) {
    classTree = msg.tree;
    updateClassList(classTree, true);
})

socket.on( 'classDataChange', function( msg ) {
    klass = msg.class;
    diag = msg.mermaidDiag;
    updateClassView(klass, diag);
})
