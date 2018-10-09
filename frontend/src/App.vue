<template>
  <v-app id="app" dark>
    <notifications group="nav" position="top center" classes="n-light" />
  
    <router-view></router-view>
    <v-dialog v-model="processed" hide-overlay persistent width="300">
      <v-card color="primary">
        <v-card-text>
          Please stand by
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  
  </v-app>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "app",
  computed: {
    ...mapState({
      processed: state => state.auth.status == "loading"
    })
  },
  methods: {
    logout: function() {
      this.$store.dispatch(AUTH_LOGOUT).then(() => {
        this.$router.push("/login");
      });
    }
  },
  mounted() {
    this.$store.dispatch("START_UP_TIME");
  }
};
</script>
