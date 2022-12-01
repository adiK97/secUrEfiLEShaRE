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

export const downloadFile = async (filename, username) => {
  return await callApi({ endpoint: 'download', method: 'post', body: { filename, username } })
}

export const getFileList = async () => {
  return await callApi({ endpoint: 'fileList', method: 'get' })
}
