// Stripe Publishable Key taken
let stripe = Stripe('pk_test_51MOjpRDh4Pu0qkGJdk7NFVquRuAFtHRjfzG67qcmxf2Q9AMog6teg0fQvayd0R0VRw09ILa9V5cX9tvebOkI7zVi001AZIRElY')

// we have button in html pay btn so we gonna take id
const submit = document.getElementById('submit')

clientsecret = submit.getAttribute('data-secret')

const elements = stripe.elements();
const style = {
    base: {
        color: '#000',
        lineHeight: '2.4',
        fontSize: '16px'
    }
}
const card = elements.create('card', {style: style})

card.mount("#card-element")

card.on('change', function(e){
    const displayError = document.getElementById('card-errors')
    if(e.error){
        displayError.textContent = e.error.message;
        $("#card-errors").addClass("alert alert-info")
    }else{
        displayError.textContent = "";
        $("#card-errors").removeClass("alert alert-info")
    }
})



submit.addEventListener("click", function(e){
    e.preventDefault()
    const firstname = document.getElementById('firstName').textContent;
    const custAdd = document.getElementById('custAdd').textContent;
    const custAdd2 = document.getElementById('custAdd2').textContent;
    const postCode = document.getElementById('postCode').textContent;
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/orders/add/",
        data: {
            order_key: clientsecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: 'post'
        },
        success: function(response){
            console.log(response);
            
            stripe.confirmCardPayment(clientsecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        address:{
                            line1: custAdd,
                            line2: custAdd2,
                        },
                        name: firstname
                    },
                }
            }).then(function(result){
                if(result.error){
                    console.log("payment Error")
                    console.log(result.error.message)
                }else{
                    if(result.paymentIntent.status === 'succeeded'){
                        console.log('payment processed')
                        window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
                    }
                }
            })
        },
        error: function(error){
            console.log(error)
        }
    })
})
