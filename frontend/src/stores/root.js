import { defineStore } from 'pinia';
import Cookies from 'js-cookie';

export const useRootStore = defineStore('root', {
  state: () => ({
    isLoading: false,
    user: {},
    isAuth: false,
    apiBaseUrl: "http://127.0.0.1:8000",
    token: Cookies.get('auth_token') || '',
    banks: []
  }),
  
  getters: {
    getUser: (state) => state.user,
    isAuthenticated: (state) => state.isAuth,
    getIsLoading: (state) => state.isLoading,
    getBanks: (state) => state.banks,
  },
  
  actions: {
    // async setUser() {
    //   if (!this.token) return;
    //   try {
    //     const response = await fetch(`${this.apiBaseUrl}/user/`, {
    //       headers: {
    //         'Authorization': `Bearer ${this.token}`,
    //         'Content-Type': 'application/json'  
    //       }
    //     });
    //     const result = await response.json();
    //     if (!result) {
    //       this.isAuth = false;
    //       Cookies.remove('auth_token');
    //     } else {
    //       this.isAuth = true;
    //       this.user = result;
    //     }
    //   } catch (error) {
    //     console.log(error);
    //   } finally {
    //     this.isLoading = false;
    //   }
    // },

    async signin(userData) {
      this.isLoading = true;
      try {
        const response = await fetch(`${this.apiBaseUrl}/auth/login/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData),
        });
        const result = await response.json();
        if (result.access_token) {
          this.token = result.access_token;
          Cookies.set('auth_token', result.access_token, { expires: 7 });
          this.isAuth = true;
        }
      } catch (err) {
        console.log(err);
        throw new Error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async signup(userData) {
      this.isLoading = true;
      try {
        const response = await fetch(`${this.apiBaseUrl}/auth/signup/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData),
        });
        const result = await response.json();
        if (result.access_token) {
          this.token = result.access_token;
          Cookies.set('auth_token', result.access_token, { expires: 7 });
          this.isAuth = true;
        }
      } catch (err) {
        console.log(err);
        throw new Error(err);
      } finally {
        this.isLoading = false;
      }
    },

    async setBanks() {
      try {
        const response = await fetch(`${this.apiBaseUrl}/banks/connections/`, {
          headers: {
            'authorisation': `Bearer ${this.token}`,
            'Content-Type': 'application/json'  
          }
        })
        const result = await response.json();
        if (result) {
          this.banks = result;
        }
      } catch(err) {
        console.log(err)
      }
    },
    async fetchBanks(bankName) {
      try {
        const response = await fetch(`${this.apiBaseUrl}/banks/auth/`, {
          method: "POST",
          headers: {
            'authorisation': `Bearer ${this.token}`,
            'Content-Type': 'application/json'  
          },
          body: JSON.stringify({bank_name: bankName}),
        })
        const result = await response.json();
        console.log(result);
      } catch(err) {
        console.log(err)
      }
    }
  }
})