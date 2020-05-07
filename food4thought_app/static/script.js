var counter = 1;
var limit = 20;
var ingredient_name_counter = 0;
var volume_counter = 0;
var measurement_counter = 0;
function addInput(divName){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Ingrediens " + (counter + 1) + ": "
          + "<input type='text' id='ingredient_name' name='ingredient_name" + (ingredient_name_counter + 1) + "'>" 
          + " Mängd: " + "<input type='text' id='volume' name='volume" + (volume_counter + 1) + "'>"
          + " Mått: " + "<input type='text' id='measurement' name='measurement" + (measurement_counter + 1) + "'>";
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}