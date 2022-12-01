import { callApi } from './callApi';

export const loginUserAPI = async (username, password) => {
  return await callApi({ endpoint: 'login', method: 'post', body: { username, password } })
}

export const createUserAPI = async (username, password) => {
  return await callApi({ endpoint: 'addUser', method: 'post', body: { username, password } })
}

export const sendFile = async (formData) => {
  return await callApi({ endpoint: 'uploadFile', method: 'post', body: formData })
}
