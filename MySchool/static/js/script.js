function confirmDelete() {

    return confirm(
        "Are you sure you want to delete this student?"
    );
}


document.addEventListener(
    "DOMContentLoaded",
    function () {

        const alerts =
            document.querySelectorAll(
                ".success-alert, .alert"
            );

        alerts.forEach(function (alert) {

            setTimeout(function () {

                alert.style.opacity = "0";

                setTimeout(function () {

                    alert.remove();

                }, 500);

            }, 4000);

        });

    }
);