function deleteService(serviceId){
    if (window.confirm(`Jeste li sigurni da želite obirsati uslugu ${serviceId}?`)) {
        fetch('/services/' + serviceId + '/deleted', {
            method: 'DELETE',
        }).then(() => {
            const path = window.location.pathname;
            const pattern = new RegExp('^/services/\\d+$');
            if (pattern.test(path)) {
                window.location.replace("/services/");
            } else {
                window.location.reload();
            }
        })
    }
}

function updateService(serviceId){
    const name = document.getElementById("name").value;
    const price = document.getElementById("price").value;
    const params = new URLSearchParams({
        name: name,
        price: price
    });
    fetch('/services/' + serviceId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: params
    }).then(() => {
        window.location.replace(`/services/${serviceId}`);
    })
}

function deleteReservation(reservationId){
    if (window.confirm(`Jeste li sigurni da želite obirsati rezervaciju ${reservationId}?`)){
        fetch('/reservations/' + reservationId + '/deleted', {
            method: 'DELETE',
        }).then(() => {
            const path = window.location.pathname;
            const pattern = new RegExp('^/reservations/\\d+$');
            if (pattern.test(path)) {
                window.location.replace("/reservations/");
            } else {
                window.location.reload();
            }
        })
    }
}

function updateReservation(reservationId){
    const id_employee = document.getElementById("id_employee").value;
    const id_customer = document.getElementById("id_customer").value;
    const reservation_date = document.getElementById("reservation_date").value;
    const id_service = document.getElementById("id_service").value;

    const params = new URLSearchParams({
        id_employee: id_employee,
        id_customer: id_customer,
        reservation_date: reservation_date,
        id_service: id_service
    });
    fetch('/reservations/' + reservationId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: params
    }).then(() => {
        window.location.replace(`/sendMail?reservation_id=${reservationId}&update=True`);
    })
}

function deleteCustomer(customerId){
    if (window.confirm(`Jeste li sigurni da želite obirsati mušteriju ${customerId}?`)) {
        fetch('/customers/' + customerId + '/deleted', {
            method: 'DELETE',
        }).then(() => {
            const path = window.location.pathname;
            const pattern = new RegExp('^/customers/\\d+$');
            if (pattern.test(path)) {
                window.location.replace("/customers/");
            } else {
                window.location.reload();
            }
        })
    }
}

function updateCustomer(customerId){
    const name = document.getElementById("name").value;
    const surname = document.getElementById("surname").value;
    const number = document.getElementById("number").value;
    const email = document.getElementById("email").value;
    const params = new URLSearchParams({
        name: name,
        surname: surname,
        number: number,
        email: email
    });
    fetch('/customers/' + customerId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: params
    }).then(() => {
        window.location.replace(`/customers/${customerId}`);
    })
}

function deleteEmployee(employeeId){
    if (window.confirm(`Jeste li sigurni da želite obirsati frizera ${employeeId}?`)) {
        fetch('/employees/' + employeeId + '/deleted', {
            method: 'DELETE',
        }).then(() => {
            const path = window.location.pathname;
            const pattern = new RegExp('^/employees/\\d+$');
            if (pattern.test(path)) {
                window.location.replace("/employees/");
            } else {
                window.location.reload();
            }
        })
    }
}

function updateEmployee(employeeId){
    const name = document.getElementById("name").value;
    const surname = document.getElementById("surname").value;
    const number = document.getElementById("number").value;
    const email = document.getElementById("email").value;
    const title = document.getElementById("title").value;
    const params = new URLSearchParams({
        name: name,
        surname: surname,
        number: number,
        email: email,
        title: title
    });
    fetch('/employees/' + employeeId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: params
    }).then(() => {
        window.location.replace(`/employees/${employeeId}`);
    })
}