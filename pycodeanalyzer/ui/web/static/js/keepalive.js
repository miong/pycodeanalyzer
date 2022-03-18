async function getRequest(url = '') {
	const response = await fetch(url, {
		method: 'GET',
		cache: 'no-cache',
	});
	return response.json();
}

document.addEventListener('DOMContentLoaded', () => {
	const url = document.location;
	const route = '/flaskwebgui-keep-server-alive';
	const intervalRequest = 3 * 1000; // Sec

	function keepAliveServer() {
		getRequest(url + route);
	}

	setInterval(keepAliveServer, intervalRequest)();
});
