
function get_matrix(){
    document.querySelector("#error").innerText = "Получаю матрицу";
    let matrix =[];
    document
        .querySelectorAll(".matrix_row")
        .forEach(matrix_row => {
            let row = [];
            for (child of matrix_row.children) {
                row.push(Number(child.firstChild.getElementsByTagName("input").value));
            }
            matrix.push(row);
        });
    return matrix;
}

function clear_system(){
     document.querySelector("#error").innerText += "Очищаю матрицу";
     document
         .querySelectorAll(".slau_element")
         .forEach(function (item){
             item.value ="";
         })

}

function get_vector(){
    document.querySelector("#error").innerText += "Получаю вектор";
    let vector =[];
    document.querySelectorAll(".vector_element")
        .forEach(vector_element =>{
            vector.push(Number(vector_element.value));
        });
    return vector;
}

function show_error(message){
    document.querySelector("#error").innerText = message;
}

function output_solution(result){
      document.querySelector("#result").innerText = "Ответ: ( " + result.join(', ') + " )";
    for (let x in result)
    {
         if( result.hasOwnProperty(x) ) {
             $('#result tbody').append('<tr><td>' + x + '</td></tr>');
         }
    }
}

function output_steps(reverse_step,d){

    for (let y in reverse_step)
    {
         if( reverse_step.hasOwnProperty(y) ) {
             $('#reverse > tr:last-child').append('<td/' + y + '>');
         }
    }
    for(let elem in d)
    {
         if( reverse_step.hasOwnProperty(d) ) {
             $('#straight > tr:last-child').append('<td/' + elem + '>');
         }
    }
}

function solve_system(){
    let slau_matrix = get_matrix();
    let vector = get_vector();
    let system = {
    "matrix":slau_matrix,
    "vector":vector
};
    fetch('/solve',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(system)
    })
        .then(response =>{
            if(!response.ok){
                throw response;
            }
            return response.json();
        })
        .then(solution => output_solution(solution.result))
        .then(solution => output_steps(solution.Y, solution.d))
        .catch(error => error.json().then(error_json => show_error(error_json.message)))
}
