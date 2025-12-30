function addToCart(id, name, price) {
    event.preventDefault()

    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        if (data.code === 400) {
        }

        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
    }).catch(function(err) {
        console.error(err)
    })
}

function updateCart(productId, obj) {
    let quantity = parseInt(obj.value);

    fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify({
            'id': productId,
            'quantity': quantity
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        // Kiểm tra code trả về từ server
        if (data.code === 400) {
            alert(data.msg); // Hiện thông báo "Tổng số lượng... không được vượt quá 10"

            // Nếu server trả về số lượng cũ, reset ô input lại
            if (data.data && data.data.old_quantity) {
                obj.value = data.data.old_quantity;
            }
        }

        let counter = document.getElementsByClassName('cart-counter');
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity;

        let amount = document.getElementById('total-amount');
        if (amount)
            amount.innerText = new Intl.NumberFormat().format(data.total_amount) + " VND";

    }).catch(err => console.error(err));
}