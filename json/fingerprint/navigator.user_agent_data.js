Object.defineProperty(Object.getPrototypeOf(navigator), "userAgentData", {
    get() {
        return {
            "brands": [{"brand": "Not_A Brand", "version": "99"}, {
                "brand": "Google Chrome",
                "version": "109"
            }, {"brand": "Chromium", "version": "109"}], "mobile": false, "platform": "macOS"
        }
    }
})
