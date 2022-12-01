import fetch from 'isomorphic-fetch';

// import {internalIpV6, internalIpV4} from 'internal-ip';

// import { HOST } from "react-dotenv"
export async function callApi({ endpoint, method = 'get', body = undefined, fullUrl = false, downloadAPI = false }) {

    let url = ''
    if (fullUrl) {
        url = endpoint;
    } else {
        url = `http://192.168.1.149:4000/${endpoint}`; // put you local ip address here
    }
    // console.log('body', body)

    if (downloadAPI) {
        return fetch(url, { method, body: JSON.stringify(body) })
            .then(response => {
                console.log('headers', response, response.headers)
                const filename = response.headers.get('Content-Disposition').split('filename=')[1];
                response.blob().then(blob => {
                    let url = window.URL.createObjectURL(blob);
                    let a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    a.click();
                });
            }).catch(err => console.log(err));
    }

    return await fetch(url, { method, body: JSON.stringify(body) })
        .then(async (response) => {
            if (!response.ok) {
                alert('An error Occured. Please verify the inputs/operation you are trying to perform.')
                return response.json()
                    .then((json) => {
                        return Promise.reject(json)
                    });
            }
            return response.json() || response.text();
        });
}