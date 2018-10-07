<template>
  <!-- <v-content class="pa-2">
                          <v-card tile>
                        
                            <div>
                              <p class="headline mb-1">{{ user }}</p>
                              <div>Located two hours south of Sydney in the Southern Highlands of New South WalesLocated two hours south of Sydney in the Southern Highlands of New South WalesLocated two hours south of Sydney in the Southern Highlands of New South WalesLocated two
                                hours south of Sydney in the Southern Highlands of New South WalesLocated two hours south of Sydney in the Southern Highlands of New South WalesLocated two hours south of Sydney in the Southern Highlands of New South WalesLocated two hours south
                                of Sydney in the Southern Highlands of New South WalesLocated two hours south of Sydney in the Southern Highlands of New South Wales , ...</div>
                            </div>
                            <v-divider v-if="ind + 1 < lenmsg" :key="`divider-${ind}`"></v-divider>
                          </v-card>
                        </v-content> -->
  
  <v-layout row>
    <div class="pt-3 px-3">
      <v-avatar v-if="!isMe(user)" slot="activator" :color="toColor(user)">
        <span class="white--text headline">{{user[0]}}</span>
        <!-- <img src="https://avatars0.githubusercontent.com/u/9064066?v=4&s=460" alt="Avatar"> -->
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
      <!-- <v-card color="secondary">
  
            </v-card> -->
    </v-flex>
  
  
  
    <!-- <v-card color="purple">
                  <v-card-text>#1</v-card-text>
                </v-card> -->
  </v-layout>
  
  
  
  <!-- <v-list-tile :key="ind" ripple>
                          <v-list-tile-content>
                            <v-list-tile-title>
                              <p class=".subheading">{{ user }}</p>
                            </v-list-tile-title>
                            <v-list-tile-title>
                              <v-card>{{ msg }}<br>{{ msg }}</v-card>
                            </v-list-tile-title>
                          </v-list-tile-content>
                          <span>{{ [time - currentTimestamp, 'seconds'] | duration('humanize', true)  }}</span>
                        </v-list-tile>
                        <v-divider v-if="ind + 1 < lenmsg" :key="`divider-${ind}`"></v-divider> -->
</template>

<script>
  import {
    mapState
  } from "vuex";
  
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
      })
    },
    methods: {
      isMe(username) {
        return username == "aazz"
      },
      toColor(str) {
        var hash = 0
        var len = str.length
        if (len === 0) return 'black'
        for (var i = 0; i < len; i++) {
          hash = ((hash << 8) - hash) + str.charCodeAt(i)
          hash |= 0
        }
        hash = Math.abs(hash)
        return '#' + hash.toString(16).substr(0, 6)
      }
    }
  };
</script>
