<template>
  <v-flex ma-0 class="chat_sc6">
    <v-card ripple height="50" @click.native="getMoreMessagess" class="chat_sc9">
      <v-container fill-height justify-center>
        <p>get more messages except events</p>
      </v-container>
    </v-card>
    <template v-for="(message, index) in messages">
      <Message
        v-if="message.type!='event'"
        :key="index"
        :ind="index"
        :user="message.user"
        :time="message.time"
        :lenmsg="messages.length"
        :msg="message.msg"
      />
      <Event
        v-else
        :key="index"
        :user="message.user"
        :time="message.time"
        :state="message.state"
        :place="message.place"
      />
    </template>
    <v-card elevation-23 class="chatsend">
      <v-text-field
        elevation-23
        hide-details
        v-if="show"
        outline
        autofocus
        loading
        solo
        label="Append"
        append-icon="send"
        v-model="mess_field"
        ref="chatform"
        @click:append="sendMessage(mess_field)"
        @keydown.enter="sendMessage(mess_field)"
      />
    </v-card>
    <p class="chat_dialog2" style="margin-bottom: 0px"></p>
  </v-flex>
</template>

<script>
import { mapState, mapActions } from "vuex";
import { MESSAGETOSERVER, GET_MORE_MESSAGES } from "store/actions/chat";
import VueScrollTo from "vue-scrollto";
import Message from "./message";
import Event from "./event";

export default {
  name: "Chat",
  components: {
    Message,
    Event
  },
  props: {
    show: {
      type: Boolean,
      default: false
    },
    containerSelector: {
      type: String,
      default: ".chat_sc77"
    }
  },
  data: function() {
    return {
      mess_field: "",
      savedHeight: 0,
      endPage: false,
      scrollState: false
    };
  },
  computed: {
    ...mapState("chat", ["messages"]),
    ...mapState({
      currentTimestamp: state => state.now / 1000
    })
  },
  watch: {
    show(val) {
      if (val) {
        this.scrollto();
      }
      console.log("show: " + val);
      return val;
    }
  },
  methods: {
    ...mapActions("chat", {
      messageToServer: MESSAGETOSERVER
    }),
    ...mapActions("chat", {
      getMoreMessages: GET_MORE_MESSAGES
    }),
    getMoreMessagess() {
      console.log("Get more messages");
      this.getMoreMessages();
    },
    sendMessage(mess) {
      if (mess.length) {
        this.messageToServer(mess);
      }
      this.mess_field = "";
    },
    updEndPage() {
      let mdiv = document.querySelector(this.containerSelector);
      this.endPage =
        Math.abs(mdiv.clientHeight - (mdiv.scrollHeight - mdiv.scrollTop)) <
        600;
    },
    scrollto() {
      var cancelScroll = VueScrollTo.scrollTo(".chat_dialog2", 1000, {
        container: this.containerSelector,
        onDone: el => {
          this.scrollState = false;
        },
        cancelable: false,
        onStart: el => {
          this.scrollState = true;
        }
      });
    }
  },
  updated() {
    if (this.endPage && !this.scrollState) {
      this.scrollto();
    }
  },
  mounted() {
    this.scrollto();
  },
  beforeUpdate() {
    this.updEndPage();
  }
};
</script>

<style>
.chatsend {
  z-index: 1;
  position: sticky;
  bottom: 0px;
}
</style>