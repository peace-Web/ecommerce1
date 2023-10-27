$(document).ready(function(){
    $("#post-form").submit(function(e){
        e.preventDefault()
        var product_qty = $("#quantity").val()
        var product_id = $("#product_id").val()
        var csrf = $("input[name = csrfmiddlewaretoken]").val()
        console.log("id: "+product_id)
        console.log("qty: "+product_qty)
        
        $.ajax({
            method:"POST",
            url: "/addtocart",
            data:{
                product_id: product_id,
                product_qty: product_qty,
                csrfmiddlewaretoken: csrf
            },
            success : function(response){
                alert(response)
            }
        })
    })

    $("#delete").submit(function(e){
        e.preventDefault()
        var prod_id = $("#prod_id").val()
        var csrfmiddlewaretoken = $("input[name = csrfmiddlewaretoken]").val()
         console.log(prod_id)
        $.ajax({
            method : "POST",
            url: "/deleteitem",
            data : {
                'prod_id': prod_id,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            success : function(response){
                console.log(response)
            }
        })
    })

    
    $( function() {
        var availableTags = []
        $.ajax({
            method: "GET",
            url: "/getproductsnames",
            
            success: function(response){
                for (item in response.products){
                    availableTags.push(response.products[item].name)
                }
                console.log(availableTags)
                $( "#search" ).autocomplete({
                    source: availableTags
                    
                  });
            }
        })
     
     
      
    } );
    

    
})