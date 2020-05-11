var counter = 1;
var limit = 20;
function addInput(){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
        counter++;
        var newdiv = document.createElement('div');
        newdiv.innerHTML = "Ingrediens " + (counter) + ": "
        + "<input type='text' id='ingredient_name' class='mt-2 mr-1' name='ingredient_name" + (counter) + "' required>" 
        + " Mängd: " + "<input type='text' id='volume' class='mt-2 mr-1' name='volume" + (counter) + "' required>"
        + " Mått: " + "<input type='text' id='measurement' class='mt-2 mr-1' name='measurement" + (counter) + "' required>";
        document.getElementById("dynamicInput").appendChild(newdiv);
     }
}

$("#add_ingredient").click(addInput);