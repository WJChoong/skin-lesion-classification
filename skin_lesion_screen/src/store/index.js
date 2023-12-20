import { createStore } from "vuex";

export default createStore({
  state: {
    isAuthenticated: false,
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
  },
  mutations: {
    SET_AUTHENTICATED(state, value) {
      state.isAuthenticated = value;
    },
  },
  actions: {
    setAuthenticated({ commit }, value) {
      commit("SET_AUTHENTICATED", value);
    },
  },
  modules: {},
});
