<template>
  <v-container fill-height @keydown.enter="login">
  
    <v-layout align-center justify-center>
  
      <v-card class="elevation-12" width="300px">
        <v-alert v-model="errorLogin" dismissible type="error">
          invalid credentials
        </v-alert>
        <v-toolbar color="success">
          <v-toolbar-title>Login</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field required prepend-icon="person" v-model="username" label="Username" type="text" :rules="[v => !!v || 'Name is required']"></v-text-field>
            <v-text-field required prepend-icon="lock" v-model="password" label="Password" type="password" :rules="[v => !!v || 'Password is required']"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <!-- {{true : }} -->
          <v-spacer></v-spacer>
          <v-btn :disabled="!valid" @click="login">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";
import { AUTH_REQUEST } from "../../store/actions/auth";

export default {
  name: "login",
  data: function() {
    return {
      errorLogin: false,
      valid: false,
      username: "aazz",
      password: "zzaa"
    };
  },
  methods: {
    ...mapActions("auth", [AUTH_REQUEST]),
    sub: function(d) {
      if (this.$refs.form.validate()) {
      }
    },
    login() {
      console.log("Try login");
      if (this.$refs.form.validate()) {
        const { username, password } = this;
        console.log(username, password);

        this.AUTH_REQUEST({
          username,
          password
        })
          .then(() => {
            this.$router.push("/home");
          })
          .catch(err => {
            this.errorLogin = true;
          });
      }
    }
  }
};
</script>

