'use strict';

const functions = require('firebase-functions');

const DialogflowApp = require('actions-on-google').DialogflowApp;

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
                                                                  
                                                                  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
                                                                  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
                                                                  
                                                                  if (request.body.result) {
                                                                        processRequest(request, response);
                                                                  
                                                                  } else {
                                                                        console.log('Invalid Request');
                                                                        return response.status(400).end('Invalid Webhook Request');
                                                                  }
                                                                  
                                                                });

function processRequest (request, response) {
    
let action = request.body.result.action;
let parameters = request.body.result.parameters;
    
let requestSource = (request.body.originalRequest) ? request.body.originalRequest.source : undefined;
const app = new DialogflowApp({request: request, response: response});
    
    
// Create handlers for Dialogflow actions as well as a 'default' handler
const actionHandlers = {
        
        'input.unknown': () => {
            sendResponse('I\'m having trouble, can you try that again?');
        },
        'find.weather': () => {
            let responseToUser = {
            speech: 'Hi! Im sorry, I do not have the weather forecast for '+parameters['geo-city']+' on '+parameters['date'],
            text: 'Hi! Im sorry, I do not have the weather forecast'
                
            };
            sendResponse(responseToUser);
        },
        // Default handler for unknown or undefined actions
        'default': () => {
            let responseToUser = {
            speech: 'This message is from Dialogflow\'s Cloud Functions for Firebase editor!',
            text: 'This is from Dialogflow\'s Cloud Functions for Firebase editor! :-)'
            };
            sendResponse(responseToUser);
        }
    };
    
    
    // If undefined or unknown action use the default handler
    if (!actionHandlers[action]) {
        action = 'default';
    }
    
    
    // Run the proper handler function to handle the request from Dialogflow
    actionHandlers[action]();
    
    
    // Function to send correctly formatted responses to Dialogflow which are then sent to the user
    function sendResponse (responseToUser) {
        
        if (typeof responseToUser === 'string') {
            
            let responseJson = {};
            responseJson.speech = responseToUser;
            responseJson.displayText = responseToUser;
            response.json(responseJson);
            
        }else {
            
            let responseJson = {};
            responseJson.speech = responseToUser.speech || responseToUser.displayText;
            responseJson.displayText = responseToUser.displayText || responseToUser.speech;
            console.log('Response to Dialogflow: ' + JSON.stringify(responseJson));
            response.json(responseJson);
        }
    }
}
