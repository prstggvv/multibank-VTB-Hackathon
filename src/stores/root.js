import {defineStore} from 'pinia';
import Cookies from 'js-cookie';

export const useRootStore = defineStore('root', {
  state: () => ({
    isLoading: false,
    user: {},
    isAuth: false,
    apiBaseUrl: "",
    token: Cookies.get('auth_token') || '',

  }),
  geters: {
    getUser: (state) => state.user,
    isAuthenticated: (state) => state.isAuth,
    getIsLoading: (state) => state.isLoading,
  },
  actions: {
    async setUser() {
      if (!this.token) return;
      try {
        const response = await fetch(`${this.apiBaseUrl}/user/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'  
          }
        });
        const result = await response.json();
        if (!result) {
          this.isAuth = false;
          Cookies.remove(auth_token);
        } else {
          this.isAuth = true;
          this.user = result;
        }
      } catch (error) {
        console.log(error);
      } finally {
        this.Loading = false;
      }
    },

    async signin(userData) {
      this.isLoading = true;
      try {
        const response = await fetch(`${this.apiBaseUrl}/signin/`, {
          method: 'POST',
          headers: {},
          body: JSON.stringify(userData),
        });
        const result = await response.json();
        Cookies.set('auth_token', result.token, { expires: 7 });
        console.log(result);
      } catch (err) {
        console.log(err)
      } finally {
        this.isLoading = false;
      }
    },

    async signin(userData) {
      this.isLoading = true;
      try {
        const response = await fetch(`${this.apiBaseUrl}/signup/`, {
          method: 'POST',
          headers: {},
          body: JSON.stringify(userData),
        });
        const result = await response.json();
        Cookies.set('auth_token', result.token, { expires: 7 });
        console.log(result);
      } catch (err) {
        console.log(err)
      } finally {
        this.isLoading = false;
      }
    }
  }
})