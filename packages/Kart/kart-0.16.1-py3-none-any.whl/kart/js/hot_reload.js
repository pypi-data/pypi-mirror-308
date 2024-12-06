function connect() {
    var timeout;

    const resetBackoff = () => {
        timeout = 1000;
    };

    const backOff = () => {
        if (timeout > 10 * 1000) {
            return;
        }

        timeout = timeout * 2;
    };

    const hotReloadUrl = () => {
        const hostAndPort =
        location.hostname + (location.port ? ":" + location.port : "");
        return "ws://" + hostAndPort + "/ws_hot_reload";
    };

    function connectHotReload() {
        const socket = new WebSocket(hotReloadUrl());

        socket.onmessage = (event) => {
            if (event.data === "reload") {
                console.log("[Hot Reloader] Server Changed, reloading");
                location.reload(true);
            }
        };

        socket.onopen = () => {
            resetBackoff();
            socket.send("Hello");
        };

        socket.onclose = () => {
            const timeoutId = setTimeout(function () {
                clearTimeout(timeoutId);
                backOff();

                connectHotReload();
            }, timeout);
        };
    }

    resetBackoff();
    connectHotReload();
};

connect();
