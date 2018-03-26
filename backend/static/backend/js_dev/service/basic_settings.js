define(['switch'], function () {
  var fn = function () {
    $.fn.bootstrapSwitch.defaults = {
      state: true,
      size: null,
      animate: true,
      disabled: false,
      readonly: false,
      indeterminate: false,
      inverse: false,
      radioAllOff: false,
      onColor: 'success',
      offColor: 'default',
      onText: '开启中',
      offText: '关闭中',
      labelText: '&nbsp',
      handleWidth: 'auto',
      labelWidth: 'auto',
      baseClass: 'bootstrap-switch',
      wrapperClass: 'wrapper',
      onInit: function onInit() {
      },
      onSwitchChange: function onSwitchChange() {
      }
    };
    $(".customer-service-switch").bootstrapSwitch();
  };
  return {
    init: fn
  };
});
