import { callApi } from './callApi';

export const loginUserAPI = async (username, password) => {
  return await callApi({ endpoint: 'login', method: 'post', body: { username, password } })
}

export const createUserAPI = async (username, password) => {
  return await callApi({ endpoint: 'addUser', method: 'post', body: { username, password } })
}

export const sendFile = async (formData) => {
  return await callApi({ endpoint: 'file', method: 'post', body: formData })
}

export const downloadFile = async (name) => {
  return await callApi({ endpoint: 'file', method: 'get', body: { filename: name } })
}

export const getFileList = async () => {
  return await callApi({ endpoint: 'fileList', method: 'get' })
}
