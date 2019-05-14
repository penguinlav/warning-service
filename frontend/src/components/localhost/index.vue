<template>
  <v-app fill-height>
    <v-container justify-center fill-height>
      <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step :complete="e1 > 1" step="1">Open link</v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step :complete="e1 > 2" step="2">Install Chrome</v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step step="3">Open site</v-stepper-step>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content step="1">
            <v-card class="mb-5">
              <v-card-text>
                Open link
                <span class="blue--text">\\srv-share.vas.local\ЦОИ\На раздачу\ПРОГРАММЫ</span> in folder on your iru
              </v-card-text>
            </v-card>
            <v-btn color="primary" @click="e1=2">Continue</v-btn>
          </v-stepper-content>
          <v-stepper-content step="2">
            <v-card class="mb-5">
              <v-card-text>
                Install
                <span class="blue--text">ChromeStandaloneSetup64.exe</span>. When it asks admin premission just to cancle it.
              </v-card-text>
            </v-card>
            <v-btn color="primary" @click="e1=3">Continue</v-btn>
          </v-stepper-content>
          <v-stepper-content step="3">
            <v-card class="mb-5">
              <v-card-text>
                Open link through Chrome
                <span class="blue--text">http://10.154.145.55:8070</span> . Congratulations!
              </v-card-text>
            </v-card>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-container>
  </v-app>
</template>


<script>
export default {
  name: "localhost",
  data() {
    return {
      e1: 0
    };
  }
};
</script>