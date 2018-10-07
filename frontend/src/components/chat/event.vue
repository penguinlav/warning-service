<template>
  <v-flex>
    <div class="text-xs-center">
          <v-chip color="primary">
            <v-avatar :color="toColor(user)" class="white--text">{{user[0].toUpperCase()}}</v-avatar>
            <span class="white--text ">{{user}} <span class="title">{{place}}</span> <span :class="(state=='on' ?'red--text': 'green--text') + ' title'">{{state}}</span> {{ [time - currentTimestamp, 'seconds'] | duration('humanize', true) }}</span>
          </v-chip>
        </div>
  </v-flex>
</template>

<script>
import { toColor } from "utils/avatar"
import { mapState } from 'vuex'
export default {
  name: "Event",
  props: {
    time: {
      type: Number
    },
    user: {
      type: String
    },
    state: {
      type: String
    },
    place: {
      type: String
    }
  },
  methods:{
    toColor
  },
  computed: {
    ...mapState({
      currentTimestamp: state => state.now / 1000
    }),
  }
}
</script>
