$(document).ready(function () {
    
    $('#add-goal-btn').click((e) => {

        if(!hasDuplicateGoal($('#goal').val().trim())){
            addGoal( $('#goal').val().trim() );
            $('#goal').val('');
        } else {
            alert('There is already a goal with the same name');
        }
    });

});


/**
 * checks for duplicate goal
 * 
 * @param {String} x new goal value
 * @returns {Boolean} true if there is duplicate otherwise false
 */
function hasDuplicateGoal(x){

    let ret = false;
    $('.goal').each((i, el) => {
        console.log(`val: ${el.value}, input: ${x}`);
        if(el.value === `goal-False-${x}`) { ret = true }
    });

    return ret;
}


/**
 * This function just generates random ID
 * 
 * @returns {String} your random ID
 */
function randomID(){
    return `random-${
        Math.floor(Math.random() * (999 - 0 + 1))
    }-random`.trim();
}


/**
 * Adds a goal checkbox on the document.
 * @param {String} newGoalName Name of the goal.
 */
function addGoal(newGoalName){

    var rID = randomID();

    if(!!newGoalName.trim()) {
        const goalTemplate = `
            <div>
                <input 
                    type="checkbox"
                    onchange="goalChanged('${rID}')"
                >
                <input
                    type="hidden"
                    name="goal-${newGoalName}"
                    id="${rID}"
                    value="goal-False-${newGoalName}"
                    class="goal"
                >
                <label for="goal-${newGoalName}">
                    ${newGoalName}
                    <span>
                        <em
                            style="color:red;"
                        >
                            new
                        </em>
                    </span>
                </label>
            </div>`;
    
        $('#goals-container').append(goalTemplate);
    }
}


/**
 * because for some reason html does not include unchecked checkbox on post 
 * we have to implement this function that replace checkboxes to a "hidden" 
 * input so the server will know if the user added a goal to the
 * task even when it is not checked.
 * 
 * @param {String} name Name of the goal.
 */
function goalChanged(id) {
    // esto tiene la culpa de los muchos días de mi sufrimiento >:(
    // apparently html does not accept period ( . ) as id i.e. "random-0.12"
    // even if converted to string. -_-
    // toggle false true val
    $(`#${id}`).val( () => {
        // fint substring True and False
        var value =  $(`#${id}`).val().trim();

        if (value.includes('False')) {
            return value.replace(/False/g, 'True');
        } else if (value.includes('True')) {
            return value.replace(/True/g, 'False');
        }
    });
}