<template>
  <v-layout row>
    <div class="pt-3 px-3">
      <v-avatar v-if="!isMe(user)" slot="activator" :color="toColor(user)">
        <span class="white--text headline">{{user[0]}}</span>
      </v-avatar>
    </div>
    <v-flex :offset-xs4="isMe(user)" xs8 py-1>
      <v-card hover>
        <v-card-title class="title pb-1">{{user}}
          <v-spacer/>
          <p class="caption">{{ [time - currentTimestamp, 'seconds'] | duration('humanize', true) }}</p>
        </v-card-title>
        <v-card-text class="py-1">{{msg}}</v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { mapState } from "vuex";
import { toColor } from "utils/avatar";
export default {
  name: "Message",

  props: {
    ind: {
      type: Number
    },
    user: {
      type: String
    },
    msg: {
      type: String
    },
    time: {
      type: Number
    },
    lenmsg: {
      type: Number
    }
  },
  computed: {
    ...mapState({
      currentTimestamp: state => state.now / 1000
    }),
    ...mapState("auth", ["profile"])
  },
  methods: {
    isMe(username) {
      return username == this.profile.username;
    },
    toColor
  }
};
</script>
