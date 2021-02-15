const LOCALHOST = 'http://localhost';
// const { API_HOST = '', ENV = 'development' } = process.env;

export interface AppConfig {
  API_ULR: string
}

const appConfig: AppConfig = {
  // API_ULR: (ENV === 'development' ? `${LOCALHOST}:8080` : API_HOST),
  API_ULR: `${LOCALHOST}:8000`,
}

export default appConfig;
