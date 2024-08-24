let stripe = Stripe("pk_test_51MOjpRDh4Pu0qkGJdk7NFVquRuAFtHRjfzG67qcmxf2Q9AMog6teg0fQvayd0R0VRw09ILa9V5cX9tvebOkI7zVi001AZIRElY")


const submit = document.getElementById("submit_one")

clientsecret = submit.getAttribute("data-secret")

const elements = stripe.elements();
const style = {
    base: {
        color: '#000',
        lineHeight: '2.4',
        fontSize: '16px'
    }
}

const card = elements.create('card', {'style': style});
card.mount('#card-element');


card.on('change', function(event){
    const displayError = document.getElementById('card-errors')
    if (event.error){
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    }else{
        displayError.textContent = '';
        $('#card-errors').removeClass('alert alert-info');
    }
});



// SELECT DELEVERY

$(`input[type=radio][name=deliveryOption]`).on('change', function(e){
    e.preventDefault()
    const delivery_id = $(this).val()
    let delivery_price = document.getElementById(`delivery_price${delivery_id}`).getAttribute("data-price")
    let product_price = document.getElementById("product_price_").getAttribute('data-product_price')
    let is_select = document.getElementById("one_click_price").getAttribute("data-isselect")
    // LOCALSTORAGE
    if (is_select === 'false'){
        let total_price = Number(delivery_price) + Number(product_price)
        let data = {"delivery_price": delivery_price, "total_price": total_price, "is_select": "true", "id": delivery_id, "product_price": product_price}
        localStorage.setItem("data", JSON.stringify(data))
        document.location.reload()
    }else{
        let data = JSON.parse(localStorage.getItem("data"))
        let delivery_price_from_local = data['delivery_price']
        if (delivery_price_from_local !== delivery_price){
            let total_price = Number(delivery_price) + Number(product_price)
            let data = {"delivery_price": delivery_price, "total_price": total_price, "is_select": "true", "id": delivery_id, "product_price": product_price}
            localStorage.setItem("data", JSON.stringify(data))
            document.location.reload()
        }

    }
    
    
    // END LOCALSTORAGE


})

// END SELECT DELEVERY

// GET DATA FROM LOCALSTORAGE
let data = JSON.parse(localStorage.getItem("data"))
let pprice = document.getElementById("product_price_").getAttribute("data-product_price")

if (data && data["product_price"] === pprice){
    document.getElementById("display-total-price").innerHTML = `$${data['total_price']}`
    document.getElementById("one_click_price").setAttribute("data-productprice", data['total_price'])
    document.getElementById("one_click_price").setAttribute("data-isselect", "true")
    $(`input[type=radio][name=deliveryOption][id=${data['id']}]`).attr("checked", true)
}

// END GET DATA FROM LOCALSTORAGE


// FORM ID WE GONNA GET ID FROM FORM

const form = document.getElementById("payment-form");
const is_select = document.getElementById("one_click_price").getAttribute("data-isselect")
if (is_select === 'true'){
    form.addEventListener('submit', function(e){
        e.preventDefault();
        const phoneNumber = document.getElementById("phonenumber").value;
        const fio = document.getElementById("fullName").value;
        const email = document.getElementById("email").value;
        const address1 = document.getElementById("custAdd").value;
        const address2 = document.getElementById("custAdd2").value;
        const country = document.getElementById("country").value;
        const postCode = document.getElementById("postCode").value;
        const total_price = document.getElementById("one_click_price").getAttribute("data-productprice");
            
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/orders/add-one-click/',
            data: {
                order_key: clientsecret,
                phoneNumber: phoneNumber,
                fio: fio,
                address1: address1,
                address2: address2,
                country: country,
                postCode: postCode,
                total_price: total_price,
                product_id: document.getElementById('on_click_product').getAttribute("data-id"),
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: 'post'
            },
            success: function(response){
                console.log(response);

                // DELETE OBJECT FROM LOCALSTORAGE
                localStorage.clear()
                // END DELETE OBJECT FROM LOCALSTORAGE
        
                stripe.confirmCardPayment(clientsecret, {
                    payment_method:{
                        card: card,
                        billing_details:{
                            address:{
                                line1: address1,
                                line2: address2,
                            },
                            name: fio
                        },
                    }
                }).then(function(result){
                    if(result.error){
                        console.log('payment error')
                        console.log(result.error.message);
                    }else{
                        if(result.paymentIntent.status === 'succeeded'){
                            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/")
                        }
                    }
                })
            },
            error: function(error){
                console.log(error)
            }
        })
    })


}else{
    const messages = document.getElementById('card-errors')
    messages.textContent = "You must select Delivery Brand!"
    messages.style.backgroundColor = 'red'
    messages.style.borderRadius = '7px'
    messages.style.color = 'white'
    messages.style.textAlign = 'center'
    setTimeout(()=>{
        messages.textContent = ''
        messages.style.backgroundColor = ''
        messages.style.borderRadius = ''
        messages.style.color = ''
        messages.style.textAlign = ''
    }, 5000)
}






