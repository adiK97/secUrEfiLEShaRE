import { callApi } from './callApi';

export const loginUserAPI = async (username, password) => {
  return await callApi({ endpoint: 'login', method: 'post', body: { username, password } })
}
