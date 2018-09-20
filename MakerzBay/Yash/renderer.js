// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

const electron = require('electron')
const { ipcRenderer: ipc, remote } = electron;
require('devtron').install();

console.log('Hello from renderer process')

document.addEventListener('keydown', function(e) {
    if(e.which === 123) {
        remote.getCurrentWindow().webContents.openDevTools();
    }
    else if(e.which == 116) {
        location.reload();
    }
});

document.querySelector('#btnSubmit').addEventListener('click', onSubmitClicked)

var response_from_service = {
                "id":1,
                "surveyFields":[
                    {
                        "id":1,
                        "fieldType":"input",
                        //"fieldLabel":"Your Name",
                        "labelName":"Name",
                        "fieldDataType":"string"
                        
                    },
                    {
                        "id":2,
                        "fieldType":"input",
                        //"fieldLabel":"Comments Textbox",
                        "labelName":"Comments",
                        "fieldDataType":"string"
                    },
                    {
                        "id":3,
                        "fieldType":"input",
                        //"fieldLabel":"Your Phone Number",
                        "labelName":"PhoneNumber",
                        "fieldDataType":"int"
                    },
                    {
                        "id":4,
                        "fieldType":"input",
                        //"fieldLabel":"Your Phone Number",
                        "labelName":"inputn1",
                        "fieldDataType":"string"
                    },
                    {
                        "id":5,
                        "fieldType":"input",
                        //"fieldLabel":"Your Phone Number",
                        "labelName":"inputn2",
                        "fieldDataType":"string"
                    },
                    {
                        "id":6,
                        "fieldType":"input",
                        //"fieldLabel":"Your Phone Number",
                        "labelName":"inputn3",
                        "fieldDataType":"string"
                    },
                    {
                        "id":7,
                        "fieldType":"input",
                        //"fieldLabel":"Your Phone Number",
                        "labelName":"inputn4",
                        "fieldDataType":"string"
                    },
                    {
                        "id":8,
                        "fieldType":"radio",
                        "labelName":"How satisfied are you",
                        "fieldDataType":"string",
                        "fieldOptions":["Excellent", "Good", "Average", "Bad"]
                    }
                ],
                "surveyStartDate":"2017-05-22T13:41:07.6177442+05:30",
                "surveyEndDate":"2017-05-27T13:41:07.6177442+05:30",
                "surveyCreatedDate":"2017-05-17T13:41:07.6167442+05:30",
                "surveyOwner":12345
                
            };

var request = require('request');

var response_from_service = '';
var form_fields = '';
var field_count = 0;
var alias = '';

request.get('http://msgsurveyapi.azurewebsites.net/api/survey',
	function (err, response, body) {
        response_from_service = body;
        response_from_service = JSON.parse(response_from_service);
        populateFields();
		//console.log(response.statusCode);
		//console.log(body);
	}
);

function populateFields(){
    form_fields = response_from_service[0]["surveyQuestions"];
    //var field_count = 0;

    var parent = document.getElementById('dynamic_content');

    for(var i=0; i<form_fields.length; i++){
        field_count++;

        create_label(form_fields[i]['questionFieldLabel'], parent);

        switch(form_fields[i]['questionFieldType']){
            case 0: {
                var input = document.createElement("input");
                input.type = "text";
                input.name = "field_name_"+ (field_count).toString();
                input.id = "field_id_" + (field_count).toString();
                parent.appendChild(input);
                break;
            }
        /*    case 'radio': {
                var form = document.createElement("form");
                form.id = "field_id_" + (field_count).toString();

                parent.appendChild(form);
                for(var j=0; j<form_fields[i]['fieldOptions'].length; j++) {
                    var input ="<input type=\"radio\" name=\""+"field_name_"+ (field_count).toString()+"\" id=\""+form_fields[i]['fieldOptions'][j]+
                    "\" value=\""+form_fields[i]['fieldOptions'][j]+"\" >";
    //                     document.createElement("input");
    //                     input.type = "radio";
    //                     input.name = "field_name_"+ (field_count).toString();
    //                     input.id = form_fields[i]['fieldOptions'][j];
    //                     input.value = form_fields[i]['fieldOptions'][j];
    // input.textContent = form_fields[i]['fieldOptions'][j].toString();
                    document.getElementById("field_id_" + (field_count).toString()).appendChild(document.createElement(input));

                    var spaceBr = document.createElement("br");
                    document.getElementById("field_id_" + (field_count).toString()).appendChild(spaceBr);
                }
                
            
            } */
        }

    }
}
//var form_fields = response_from_service['surveyFields'];


function create_label(labelName, parent) {
    var label = document.createElement("label");
    label.innerText = labelName;
    parent.appendChild(label);
}

function onSubmitClicked() {
    var json_to_post = {};
    var json_responded_by = {};
    var json_survey_responses = [];

    json_responded_by['cardId'] = '1234';
    json_responded_by['alias'] = alias;
    json_responded_by['email'] = alias;

    for(var i=0; i<field_count; i++){
        var j=i+1;
        var temp_json = {};
        temp_json['surveyQuestionId'] = form_fields[i]['id'];
        temp_json['questionFieldName'] = form_fields[i]['questionFieldName'];
        temp_json['questionFieldValue'] = document.getElementById('field_id_'+(j).toString()).value;

        json_survey_responses.push(temp_json);

    }

    json_to_post['surveyId'] = response_from_service[0]['id'];
    json_to_post['respondedBy'] = json_responded_by;
    json_to_post['surveyQuestionResponses'] = json_survey_responses;


    request({
        url: 'http://msgsurveyapi.azurewebsites.net/api/surveyresponses',
        method:  "POST",
        headers:  {"content-type":  "application/json"},
        json: json_to_post
    }, function (error, response, body) {
        console.log(body);
    });


    //var x = document.getElementById('field_id_1').value;
    alert("Submitted Successfully");
} 

ipc.on('cardId', (event, arg) => {
    alias = arg;
    alert(arg)
})
/*
var f = document.createElement("form");
f.setAttribute('method', "post");
f.setAttribute('onSubmit', "onSubmitClicked");

var i = document.createElement("input");
i.type = "text";
i.name = "field1_name";
i.id = "field1_id";

var s = document.createElement("input");
s.type = "text";
s.name = "field2_name";
s.id = "field2_id";

f.appendChild(i);
f.appendChild(s);
*/

//$("body").append(f);
//document.getElementsByTagName('body')[0].appendChild(f);