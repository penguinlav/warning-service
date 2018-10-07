<template>
  <v-container fill-height grid-list-xs pa-0 justify-center wrap v-resize="onResize" >
    <v-layout row fill-height v-if="!fullState">     
      
      <v-flex d-flex xs3>
        <v-layout column wrap>
          <v-flex d-flex>
            <v-card :class="{'headline item':true, 'red':states['lec1']}" @click.native="updState('lec1')" hover><span :hidden=hidePlaces>Сlassroom 1</span></v-card>
          </v-flex>
  
          <v-flex d-flex>
            <v-card :class="{'headline item':true, 'red':states['lec2']}" @click.native="updState('lec2')" hover><span :hidden=hidePlaces>Сlassroom 2</span></v-card>
          </v-flex>
          <v-flex d-flex>
            <v-card :class="{'headline item':true, 'red':states['lec3']}" @click.native="updState('lec3')" hover><span :hidden=hidePlaces>Сlassroom 3</span></v-card>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex d-flex xs10>
        <v-card :class="{'headline item':true}" :style="{'animation': states['cp'] ? 'blinkingBack 0.3s infinite' : '' }" @click.native="updState('cp')" hover><span :hidden=hidePlaces>Сentral passage</span></v-card>
      </v-flex>
      <v-flex d-flex xs3>
        <v-layout column wrap>
          <v-flex d-flex>
            <v-card :class="{'headline item':true, 'red':states['lab1']}" @click.native="updState('lab1')" hover><span :hidden=hidePlaces>Laboratory 1</span>
            </v-card>
          </v-flex>
          <v-flex d-flex>
            <v-card :class="{'headline item':true, 'red':states['lab2']}" @click.native="updState('lab2')" hover><span :hidden=hidePlaces>Laboratory 2</span>
            </v-card>
          </v-flex>
          <v-flex d-flex>
            <v-card :class="{'headline item':true, 'red':states['lab3']}" @click.native="updState('lab3')" hover><span :hidden=hidePlaces>Laboratory 3</span>
            </v-card>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
    <div v-else class="fullscreen" :style="{'animation': states['cp'] ? 'blinkingBack 0.3s infinite' : '' }" @click="updState('cp')" hover ripple>
    </div>
  </v-container>
</template>

<script>
  import {
    mapActions,
    mapState
  } from "vuex";
  
  export default {
    name: "CoreFeature",

    props: {
      turnOffFeatures: {
        type: Boolean,
        default: false
      },
    },
  
    data: function() {
      return {
        hidePlaces: false,
        fullState: false,
      };
    },
    computed: {
      // примешиваем геттеры в вычисляемые свойства оператором расширения
      ...mapState("core_features", ["states"])
    },
    methods: {
      ...mapActions("core_features", ["updState"]),
      // ...mapActions([START_WEBSOCKET]),
      onResize() {
        console.log("this.turnOffFeatures: " + this.turnOffFeatures);
        if (!this.turnOffFeatures) {
          this.hidePlaces = window.innerWidth <= 840;
          this.fullState = window.innerWidth <= 600 || window.innerHeight <= 400;
        } else {
          this.hidePlaces = true;
          this.fullState = false;
        }
      }
    }
  };
</script>

<style>
  .fullscreen {
    left: 0px;
    top: 0px;
    z-index: 999999;
    position: fixed;
    width: 100%;
    height: 100%;
    background-color: #ffffff;
  }
  
  body {
    margin: 0;
  }
  
  .item {
    /* border: solid; */
    -webkit-box-align: center;
    -webkit-box-pack: center;
    display: -webkit-box;
  }
  
  @keyframes blinkingBack {
    0% {
      background-color: #000000;
    }
    /* 0%{		background-color: #ffff00;	} */
    /* 49%{	color: transparent;	} */
    100% {
      background-color: #ffffff;
    }
  }
</style>
