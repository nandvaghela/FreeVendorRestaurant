let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in','us','ca']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields

    var Geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    Geocoder.geocode({'address':address}, function(results,status){
        if (status==google.maps.GeocoderStatus.OK){
            let latitude = results[0].geometry.location.lat()
            let longitude = results[0].geometry.location.lng()

            console.log("latitude:",latitude)
            console.log("longitude: ", longitude)

            $('#id_latitude').val(latitude)
            $('#id_longitude').val(longitude)

            $('#id_address').val(address)
        }
    })

    for (let i=0; i<place.address_components.length; i++){
        for(let j=0; j<place.address_components[i].types.length; i++){
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name)
            }
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name)
            }
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name)
            }
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name)
            }
            else{
                $('#id_pin_code').val("")
            }
        }
    }
}

$(document).ready(function(){
    // Add to Cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){

                if(response.status =='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }else if(response.status =='Failed'){

                    swal(response.message,'','error')
                }
                else{
                    console.log(response)
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)

                    // subtotal, tax, grand_total
                    SetCartAmounts(
                        response.cart_amount['sub_total'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        })

    })


    // Cart Item Quantity

    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })


    // Decrease to Cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id')
        cart_id = $(this).attr('id')
        url = $(this).attr('data-url')
        data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){


                if(response.status =='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }else if(response.status =='Failed'){

                    swal(response.message,'','error')
                }
                else{
                console.log(response)
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)

                    if(window.location.pathname == '/cart/'){
                        remove_cart_item(response.qty, cart_id)
                        check_cart_empty()
                    }

                     // subtotal, tax, grand_total
                    SetCartAmounts(
                        response.cart_amount['sub_total'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }

            }
        })

    })

    // Decrease to Cart
    $('.delete_cart').on('click', function(e){

        e.preventDefault();
        cart_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        data = {
            cart_id: cart_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){


                if(response.status =='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }else if(response.status =='Failed'){

                    swal(response.message,'','error')
                }
                else{
                console.log(response)
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    swal(response.status,response.message,'success')


                    if(window.location.pathname == '/cart/'){
                        remove_cart_item(response.qty, cart_id)
                        check_cart_empty()
                    }
                    // subtotal, tax, grand_total
                    SetCartAmounts(
                        response.cart_amount['sub_total'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }

            }
        })

    })

    // Remove Cart Item
    remove_cart_item = (cartItemQty, cart_id) => {
            if(cartItemQty <= 0){
                document.getElementById("item-"+cart_id).remove()
            }
    }

    // Check Cart Empty
    check_cart_empty = () => {
        let cart_counter = document.getElementById("cart_counter").innerHTML
        if(cart_counter == 0 ){
            document.getElementById("empty-cart").style.display = "block"
        }
    }

    // Check cart amounts
    SetCartAmounts = (sub_total, tax, grand_total) => {
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(sub_total)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }
    }

});
