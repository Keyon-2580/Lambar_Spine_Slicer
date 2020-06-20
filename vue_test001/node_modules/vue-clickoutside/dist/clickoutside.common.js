'use strict';

/**
 * v-clickoutside
 * @desc 点击元素外面才会触发的事件
 * @example
 * ```vue
 * <div v-element-clickoutside="show = false">
 * ```
 */
var index = {
  id: 'clickoutside',

  bind: function bind() {
    var _this = this;

    this.handler = function (e) {
      if (_this.vm && !_this.el.contains(e.target)) {
        _this.vm.$eval(_this.expression);
      }
    };
    document.addEventListener(this.arg || 'click', this.handler);
  },
  unbind: function unbind() {
    document.removeEventListener(this.arg || 'click', this.handler);
  },
  install: function install(Vue) {
    Vue.directive('clickoutside', {
      bind: this.bind,
      unbind: this.unbind
    });
  }
};

module.exports = index;