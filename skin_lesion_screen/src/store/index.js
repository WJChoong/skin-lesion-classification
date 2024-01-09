import { createStore } from "vuex";

export default createStore({
  state: {
    isAuthenticated: false,
    user_level: null,
    user_id: null,
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    user_level: (state) => state.user_level,
    user_id: (state) => state.user_id,
  },
  mutations: {
    SET_AUTHENTICATED(state, value) {
      state.isAuthenticated = value;
    },
    SET_USER_LEVEL(state, level) {
      state.user_level = level;
    },
    SET_USER_ID(state, id) {
      state.user_id = id;
    },
    clearUserData(state) {
      state.isAuthenticated = false;
      state.user_level = null;
      state.user_id = null;
    },
  },
  actions: {
    setAuthenticated({ commit }, value) {
      commit("SET_AUTHENTICATED", value);
    },
    setUserLevel({ commit }, level) {
      commit("SET_USER_LEVEL", level);
    },
    setUserId({ commit }, id) {
      commit("SET_USER_ID", id);
    },
  },
  modules: {},
});
