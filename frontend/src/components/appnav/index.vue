<template>
  <v-content>
    <v-navigation-drawer v-model="sidebar" app>
      <v-list>
        <v-list-tile v-for="item in menuItems" :key="item.title" :to="item.path">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>{{ item.title }}</v-list-tile-content>
        </v-list-tile>
        <v-list-tile v-for="(item, key, index) in users" :key="key">
          <v-list-tile-content>
            <div class="text-xs-center">
              <v-chip
                color="green"
                :close="profile.username=='lavrov'"
                @input="forceLogOut(item.username, key)"
              >
                <v-avatar
                  :color="toColor(item.username)"
                  class="white--text"
                >{{item.username[0].toUpperCase()}}</v-avatar>
                <span class="white--text">{{item.username}}</span>
                <span class="pa-3">online</span>
                <span class="pa-0">#{{key.slice(0,3)}}</span>
              </v-chip>
            </div>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar app :color="colors[color]" ripple>
      <span>
        <v-toolbar-side-icon @click="sidebar = !sidebar"></v-toolbar-side-icon>
      </span>
      <v-toolbar-title>
        <v-btn flat to="/changelog">
          Changelog
          <v-icon right dark>assignment</v-icon>
        </v-btn>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-title class="green--text" v-if="isConnected" @click="changeColorToolbar">
        Connected
        <v-icon class="green--text">check_circle</v-icon>
      </v-toolbar-title>
      <v-toolbar-title
        class="red--text"
        v-else
        style="animation: blinking 1s infinite"
        @click="changeColorToolbar"
      >
        Disconnect
        <v-icon class="red--text">report_problem</v-icon>
      </v-toolbar-title>
      <v-toolbar-items></v-toolbar-items>
      <v-toolbar-items :class="(isAFK ? 'yellow' : '') +   ' hidden-xs-only' ">
        <v-btn flat @click.native="updState('afk')">{{(isAFK)? 'AFK': 'Here'}}</v-btn>
      </v-toolbar-items>

      <v-toolbar-items class="hidden-xs-only">
        <v-btn flat v-for="item in menuItems" :key="item.title" :to="item.path">
          <v-icon left dark>{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-btn>
        <v-btn flat @click="userSignOut" v-if="isAuthenticated">
          <v-icon left>exit_to_app</v-icon>Sign Out
        </v-btn>
        <v-btn icon large>
          <v-avatar size="32px" :color="toColor(profile.username)">
            <span class="white--text headline">{{profile.username[0]}}</span>
          </v-avatar>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-fab-transition>
      <v-btn
        round
        style="z-index: 9999"
        class="float-chat"
        small
        color="pink"
        v-show="this.$router.currentRoute.path!='/chat'"
        bottom
        fixed
        right
        large
        @click="dialog=true"
      >
        <v-badge v-model="count" overlap>
          <span slot="badge">{{count}}</span>
          <v-icon>chat</v-icon>
        </v-badge>
      </v-btn>
    </v-fab-transition>
    <v-dialog
      ma-0
      content-class="chat_dialog"
      v-model="dialog"
      width="500"
      @keydown.esc="dialog=false"
    >
      <Chat containerSelector=".chat_dialog" :show="dialog"/>
    </v-dialog>
    <notifications group="chat" position="bottom right" classes="n-light mess"/>

    <v-container fill-height>
      <router-view name="workspace"></router-view>
    </v-container>

    <notifications group="event" classes="n-light"/>
  </v-content>
</template>

<script>
import { mapGetters, mapActions, mapState, mapMutations } from "vuex";
import { AUTH_LOGOUT, GET_PROFILE } from "store/actions/auth";
import { START_WEBSOCKET } from "store/actions/default";
import { OPEN_CHAT, CLOSE_CHAT } from "store/mutations/chat";
import { SET_CHAT_DIALOG } from "store/actions/chat";
import { toColor } from "utils/avatar";
import CoreFeature from "components/corefeature";
import Chat from "components/chat";

export default {
  components: {
    CoreFeature,
    Chat
  },
  data: function() {
    return {
      appTitle: "Awesome App",
      sidebar: false,
      show: true,
      chatCount: 2,
      color: 0,
      colors: [
        "",
        "red",
        "pink",
        "purple",
        "deep-purple",
        "indigo",
        "blue",
        "light-blue",
        "cyan",
        "teal",
        "green",
        "light-green",
        "lime",
        "yellow",
        "amber",
        "orange",
        "deep-orange",
        "brown",
        "blue-grey",
        "grey"
      ]
    };
  },
  computed: {
    ...mapState(["isConnected"]),
    ...mapState("chat", ["count"]),
    ...mapState("chat", ["users"]),
    ...mapState("auth", ["profile"]),
    ...mapGetters("core_features", ["isAFK"]),
    dialog: {
      get() {
        return this.$store.state.chat.isDialogShow;
      },
      set(value) {
        this.SET_CHAT_DIALOG(value);
      }
    },
    ...mapGetters("auth", ["isAuthenticated"]),
    menuItems() {
      if (this.isAuthenticated) {
        return [
          {
            title: "Home",
            path: "/home",
            icon: "home"
          }
        ];
      } else {
        return [
          {
            title: "Sign Up",
            path: "/signup",
            icon: "face"
          },
          {
            title: "Sign In",
            path: "/signin",
            icon: "lock_open"
          }
        ];
      }
    }
  },
  methods: {
    ...mapActions([START_WEBSOCKET]),
    ...mapActions("core_features", ["updState"]),
    ...mapActions("auth", [AUTH_LOGOUT, GET_PROFILE]),
    ...mapActions("chat", [SET_CHAT_DIALOG]),
    ...mapMutations("chat", [OPEN_CHAT, CLOSE_CHAT]),
    userSignOut() {
      console.log("AUTH_LOGOUT");
      this.AUTH_LOGOUT().then(() => {
        console.log("disp");
      });
    },
    changeColorToolbar() {
      console.log("pr: ", this.profile);
      this.color = (this.color + 1) % this.colors.length;
    },
    toColor,
    forceLogOut(username, id) {
      console.log(
        `Волею, дарованной мне создателем, кикаю ${username} #${id.slice(0, 3)}`
      );
      this.$socket.emit("forcelogout", id);
    }
  },
  mounted() {
    console.log("mount nav");
    console.log(this.START_WEBSOCKET);
    this.GET_PROFILE();
    this.START_WEBSOCKET();
  }
};
</script>

<style>
@keyframes blinking {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 100;
  }
}

.notification.n-light {
  margin: 10px;
  margin-bottom: 0;
  border-radius: 3px;
  font-size: 25px;
  padding: 10px 20px;
  background: #eaf4fe;
  border: 1px solid #d4e8fd;
}

.notification.mess {
  color: rgb(45, 47, 45);
}

.notification-title {
  letter-spacing: 1px;
  text-transform: uppercase;
  font-size: 20px;
}
</style>
