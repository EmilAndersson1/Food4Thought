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
        + "<input type='text' id='ingredient_name' name='ingredient_name" + (counter) + "'>" 
        + " Mängd: " + "<input type='text' id='volume' name='volume" + (counter) + "'>"
        + " Mått: " + "<input type='text' id='measurement' name='measurement" + (counter) + "'>";
        document.getElementById("dynamicInput").appendChild(newdiv);
     }
}

$("#add_ingredient").click(addInput);