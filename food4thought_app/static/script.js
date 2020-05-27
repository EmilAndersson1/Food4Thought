var counter = 1;
var limit = 20;

$(document).ready(function(){
     $("#add_ingredient").off('click').on('click', function(){
          if (counter == limit)  {
               alert("You have reached the limit of adding " + counter + " inputs");
          }
          else {
             counter++;
             $("#dynamicInput").append(
               "<div class='form-row'>" +
               "<div class='col-md-3'>" + "<label for='ingredient_name'>" +  "Ingrediens " + (counter) + "</label>" + ": "
               + "<input type='text' id='ingredient_name' class='mt-2 mr-1 form-control' name='ingredient_name" + (counter) + "' required>" + "</div>" 
               + "<div class='col-md-1'>" +  "<label for='volume'>" +" Mängd: " + "</label>" + "<input type='text' id='volume' class='mt-2 mr-1 form-control' name='volume" + (counter) + "' required>" + "</div>"
               + "<div class='col-md-1'>" + "<label for='measurement'>" +" Mått: " + "</label>" + "<input type='text' id='measurement' class='mt-2 mr-1 form-control' name='measurement" + (counter) + "' required>" + "</div>"
               + "</div>"
             );
          }
          return false;
     });
})

$('input[type="file"]').change(function(e){
     var fileName = e.target.files[0].name;
     $('.custom-file-label').html(fileName);
 });