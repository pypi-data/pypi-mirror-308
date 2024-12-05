/*! For license information please see GLI4E-_4.js.LICENSE.txt */
export const id=233;export const ids=[233];export const modules={5429:(t,e,i)=>{i.d(e,{Jv:()=>n,OK:()=>o,P$:()=>r,Y7:()=>s,nL:()=>a});var n,o,s={ANCHOR:"mdc-menu-surface--anchor",ANIMATING_CLOSED:"mdc-menu-surface--animating-closed",ANIMATING_OPEN:"mdc-menu-surface--animating-open",FIXED:"mdc-menu-surface--fixed",IS_OPEN_BELOW:"mdc-menu-surface--is-open-below",OPEN:"mdc-menu-surface--open",ROOT:"mdc-menu-surface"},r={CLOSED_EVENT:"MDCMenuSurface:closed",CLOSING_EVENT:"MDCMenuSurface:closing",OPENED_EVENT:"MDCMenuSurface:opened",OPENING_EVENT:"MDCMenuSurface:opening",FOCUSABLE_ELEMENTS:["button:not(:disabled)",'[href]:not([aria-disabled="true"])',"input:not(:disabled)","select:not(:disabled)","textarea:not(:disabled)",'[tabindex]:not([tabindex="-1"]):not([aria-disabled="true"])'].join(", ")},a={TRANSITION_OPEN_DURATION:120,TRANSITION_CLOSE_DURATION:75,MARGIN_TO_EDGE:32,ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO:.67,TOUCH_EVENT_WAIT_MS:30};!function(t){t[t.BOTTOM=1]="BOTTOM",t[t.CENTER=2]="CENTER",t[t.RIGHT=4]="RIGHT",t[t.FLIP_RTL=8]="FLIP_RTL"}(n||(n={})),function(t){t[t.TOP_LEFT=0]="TOP_LEFT",t[t.TOP_RIGHT=4]="TOP_RIGHT",t[t.BOTTOM_LEFT=1]="BOTTOM_LEFT",t[t.BOTTOM_RIGHT=5]="BOTTOM_RIGHT",t[t.TOP_START=8]="TOP_START",t[t.TOP_END=12]="TOP_END",t[t.BOTTOM_START=9]="BOTTOM_START",t[t.BOTTOM_END=13]="BOTTOM_END"}(o||(o={}))},487:(t,e,i)=>{i.d(e,{M:()=>m});var n=i(6513),o=i(4943),s={ROOT:"mdc-form-field"},r={LABEL_SELECTOR:".mdc-form-field > label"};const a=function(t){function e(i){var o=t.call(this,(0,n.Cl)((0,n.Cl)({},e.defaultAdapter),i))||this;return o.click=function(){o.handleClick()},o}return(0,n.C6)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return s},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return r},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},e.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},e.prototype.handleClick=function(){var t=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){t.adapter.deactivateInputRipple()}))},e}(o.I);var d=i(1086),c=i(7653),l=i(6584),h=i(8597),u=i(196),p=i(9760);class m extends d.O{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=a}createAdapter(){return{registerInteractionHandler:(t,e)=>{this.labelEl.addEventListener(t,e)},deregisterInteractionHandler:(t,e)=>{this.labelEl.removeEventListener(t,e)},activateInputRipple:async()=>{const t=this.input;if(t instanceof c.ZS){const e=await t.ripple;e&&e.startPress()}},deactivateInputRipple:async()=>{const t=this.input;if(t instanceof c.ZS){const e=await t.ripple;e&&e.endPress()}}}}get input(){var t,e;return null!==(e=null===(t=this.slottedInputs)||void 0===t?void 0:t[0])&&void 0!==e?e:null}render(){const t={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return h.qy`
      <div class="mdc-form-field ${(0,p.H)(t)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}click(){this._labelClick()}_labelClick(){const t=this.input;t&&(t.focus(),t.click())}}(0,n.Cg)([(0,u.MZ)({type:Boolean})],m.prototype,"alignEnd",void 0),(0,n.Cg)([(0,u.MZ)({type:Boolean})],m.prototype,"spaceBetween",void 0),(0,n.Cg)([(0,u.MZ)({type:Boolean})],m.prototype,"nowrap",void 0),(0,n.Cg)([(0,u.MZ)({type:String}),(0,l.P)((async function(t){var e;null===(e=this.input)||void 0===e||e.setAttribute("aria-label",t)}))],m.prototype,"label",void 0),(0,n.Cg)([(0,u.P)(".mdc-form-field")],m.prototype,"mdcRoot",void 0),(0,n.Cg)([(0,u.gZ)("",!0,"*")],m.prototype,"slottedInputs",void 0),(0,n.Cg)([(0,u.P)("label")],m.prototype,"labelEl",void 0)},4258:(t,e,i)=>{i.d(e,{R:()=>n});const n=i(8597).AH`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch[dir=rtl]){margin-left:10px}`},6038:(t,e,i)=>{var n=i(6513),o=i(196),s=(i(7432),i(5429)),r=i(4943),a=function(t){function e(i){var o=t.call(this,(0,n.Cl)((0,n.Cl)({},e.defaultAdapter),i))||this;return o.isSurfaceOpen=!1,o.isQuickOpen=!1,o.isHoistedElement=!1,o.isFixedPosition=!1,o.isHorizontallyCenteredOnViewport=!1,o.maxHeight=0,o.openBottomBias=0,o.openAnimationEndTimerId=0,o.closeAnimationEndTimerId=0,o.animationRequestId=0,o.anchorCorner=s.OK.TOP_START,o.originCorner=s.OK.TOP_START,o.anchorMargin={top:0,right:0,bottom:0,left:0},o.position={x:0,y:0},o}return(0,n.C6)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return s.Y7},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return s.P$},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return s.nL},enumerable:!1,configurable:!0}),Object.defineProperty(e,"Corner",{get:function(){return s.OK},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},hasClass:function(){return!1},hasAnchor:function(){return!1},isElementInContainer:function(){return!1},isFocused:function(){return!1},isRtl:function(){return!1},getInnerDimensions:function(){return{height:0,width:0}},getAnchorDimensions:function(){return null},getWindowDimensions:function(){return{height:0,width:0}},getBodyDimensions:function(){return{height:0,width:0}},getWindowScroll:function(){return{x:0,y:0}},setPosition:function(){},setMaxHeight:function(){},setTransformOrigin:function(){},saveFocus:function(){},restoreFocus:function(){},notifyClose:function(){},notifyClosing:function(){},notifyOpen:function(){},notifyOpening:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){var t=e.cssClasses,i=t.ROOT,n=t.OPEN;if(!this.adapter.hasClass(i))throw new Error(i+" class required in root element.");this.adapter.hasClass(n)&&(this.isSurfaceOpen=!0)},e.prototype.destroy=function(){clearTimeout(this.openAnimationEndTimerId),clearTimeout(this.closeAnimationEndTimerId),cancelAnimationFrame(this.animationRequestId)},e.prototype.setAnchorCorner=function(t){this.anchorCorner=t},e.prototype.flipCornerHorizontally=function(){this.originCorner=this.originCorner^s.Jv.RIGHT},e.prototype.setAnchorMargin=function(t){this.anchorMargin.top=t.top||0,this.anchorMargin.right=t.right||0,this.anchorMargin.bottom=t.bottom||0,this.anchorMargin.left=t.left||0},e.prototype.setIsHoisted=function(t){this.isHoistedElement=t},e.prototype.setFixedPosition=function(t){this.isFixedPosition=t},e.prototype.isFixed=function(){return this.isFixedPosition},e.prototype.setAbsolutePosition=function(t,e){this.position.x=this.isFinite(t)?t:0,this.position.y=this.isFinite(e)?e:0},e.prototype.setIsHorizontallyCenteredOnViewport=function(t){this.isHorizontallyCenteredOnViewport=t},e.prototype.setQuickOpen=function(t){this.isQuickOpen=t},e.prototype.setMaxHeight=function(t){this.maxHeight=t},e.prototype.setOpenBottomBias=function(t){this.openBottomBias=t},e.prototype.isOpen=function(){return this.isSurfaceOpen},e.prototype.open=function(){var t=this;this.isSurfaceOpen||(this.adapter.notifyOpening(),this.adapter.saveFocus(),this.isQuickOpen?(this.isSurfaceOpen=!0,this.adapter.addClass(e.cssClasses.OPEN),this.dimensions=this.adapter.getInnerDimensions(),this.autoposition(),this.adapter.notifyOpen()):(this.adapter.addClass(e.cssClasses.ANIMATING_OPEN),this.animationRequestId=requestAnimationFrame((function(){t.dimensions=t.adapter.getInnerDimensions(),t.autoposition(),t.adapter.addClass(e.cssClasses.OPEN),t.openAnimationEndTimerId=setTimeout((function(){t.openAnimationEndTimerId=0,t.adapter.removeClass(e.cssClasses.ANIMATING_OPEN),t.adapter.notifyOpen()}),s.nL.TRANSITION_OPEN_DURATION)})),this.isSurfaceOpen=!0))},e.prototype.close=function(t){var i=this;if(void 0===t&&(t=!1),this.isSurfaceOpen){if(this.adapter.notifyClosing(),this.isQuickOpen)return this.isSurfaceOpen=!1,t||this.maybeRestoreFocus(),this.adapter.removeClass(e.cssClasses.OPEN),this.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),void this.adapter.notifyClose();this.adapter.addClass(e.cssClasses.ANIMATING_CLOSED),requestAnimationFrame((function(){i.adapter.removeClass(e.cssClasses.OPEN),i.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),i.closeAnimationEndTimerId=setTimeout((function(){i.closeAnimationEndTimerId=0,i.adapter.removeClass(e.cssClasses.ANIMATING_CLOSED),i.adapter.notifyClose()}),s.nL.TRANSITION_CLOSE_DURATION)})),this.isSurfaceOpen=!1,t||this.maybeRestoreFocus()}},e.prototype.handleBodyClick=function(t){var e=t.target;this.adapter.isElementInContainer(e)||this.close()},e.prototype.handleKeydown=function(t){var e=t.keyCode;("Escape"===t.key||27===e)&&this.close()},e.prototype.autoposition=function(){var t;this.measurements=this.getAutoLayoutmeasurements();var i=this.getoriginCorner(),n=this.getMenuSurfaceMaxHeight(i),o=this.hasBit(i,s.Jv.BOTTOM)?"bottom":"top",r=this.hasBit(i,s.Jv.RIGHT)?"right":"left",a=this.getHorizontalOriginOffset(i),d=this.getVerticalOriginOffset(i),c=this.measurements,l=c.anchorSize,h=c.surfaceSize,u=((t={})[r]=a,t[o]=d,t);l.width/h.width>s.nL.ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO&&(r="center"),(this.isHoistedElement||this.isFixedPosition)&&this.adjustPositionForHoistedElement(u),this.adapter.setTransformOrigin(r+" "+o),this.adapter.setPosition(u),this.adapter.setMaxHeight(n?n+"px":""),this.hasBit(i,s.Jv.BOTTOM)||this.adapter.addClass(e.cssClasses.IS_OPEN_BELOW)},e.prototype.getAutoLayoutmeasurements=function(){var t=this.adapter.getAnchorDimensions(),e=this.adapter.getBodyDimensions(),i=this.adapter.getWindowDimensions(),n=this.adapter.getWindowScroll();return t||(t={top:this.position.y,right:this.position.x,bottom:this.position.y,left:this.position.x,width:0,height:0}),{anchorSize:t,bodySize:e,surfaceSize:this.dimensions,viewportDistance:{top:t.top,right:i.width-t.right,bottom:i.height-t.bottom,left:t.left},viewportSize:i,windowScroll:n}},e.prototype.getoriginCorner=function(){var t,i,n=this.originCorner,o=this.measurements,r=o.viewportDistance,a=o.anchorSize,d=o.surfaceSize,c=e.numbers.MARGIN_TO_EDGE;this.hasBit(this.anchorCorner,s.Jv.BOTTOM)?(t=r.top-c+this.anchorMargin.bottom,i=r.bottom-c-this.anchorMargin.bottom):(t=r.top-c+this.anchorMargin.top,i=r.bottom-c+a.height-this.anchorMargin.top),!(i-d.height>0)&&t>i+this.openBottomBias&&(n=this.setBit(n,s.Jv.BOTTOM));var l,h,u=this.adapter.isRtl(),p=this.hasBit(this.anchorCorner,s.Jv.FLIP_RTL),m=this.hasBit(this.anchorCorner,s.Jv.RIGHT)||this.hasBit(n,s.Jv.RIGHT),f=!1;(f=u&&p?!m:m)?(l=r.left+a.width+this.anchorMargin.right,h=r.right-this.anchorMargin.right):(l=r.left+this.anchorMargin.left,h=r.right+a.width-this.anchorMargin.left);var g=l-d.width>0,y=h-d.width>0,T=this.hasBit(n,s.Jv.FLIP_RTL)&&this.hasBit(n,s.Jv.RIGHT);return y&&T&&u||!g&&T?n=this.unsetBit(n,s.Jv.RIGHT):(g&&f&&u||g&&!f&&m||!y&&l>=h)&&(n=this.setBit(n,s.Jv.RIGHT)),n},e.prototype.getMenuSurfaceMaxHeight=function(t){if(this.maxHeight>0)return this.maxHeight;var i=this.measurements.viewportDistance,n=0,o=this.hasBit(t,s.Jv.BOTTOM),r=this.hasBit(this.anchorCorner,s.Jv.BOTTOM),a=e.numbers.MARGIN_TO_EDGE;return o?(n=i.top+this.anchorMargin.top-a,r||(n+=this.measurements.anchorSize.height)):(n=i.bottom-this.anchorMargin.bottom+this.measurements.anchorSize.height-a,r&&(n-=this.measurements.anchorSize.height)),n},e.prototype.getHorizontalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,s.Jv.RIGHT),n=this.hasBit(this.anchorCorner,s.Jv.RIGHT);if(i){var o=n?e.width-this.anchorMargin.left:this.anchorMargin.right;return this.isHoistedElement||this.isFixedPosition?o-(this.measurements.viewportSize.width-this.measurements.bodySize.width):o}return n?e.width-this.anchorMargin.right:this.anchorMargin.left},e.prototype.getVerticalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,s.Jv.BOTTOM),n=this.hasBit(this.anchorCorner,s.Jv.BOTTOM);return i?n?e.height-this.anchorMargin.top:-this.anchorMargin.bottom:n?e.height+this.anchorMargin.bottom:this.anchorMargin.top},e.prototype.adjustPositionForHoistedElement=function(t){var e,i,o=this.measurements,s=o.windowScroll,r=o.viewportDistance,a=o.surfaceSize,d=o.viewportSize,c=Object.keys(t);try{for(var l=(0,n.Ju)(c),h=l.next();!h.done;h=l.next()){var u=h.value,p=t[u]||0;!this.isHorizontallyCenteredOnViewport||"left"!==u&&"right"!==u?(p+=r[u],this.isFixedPosition||("top"===u?p+=s.y:"bottom"===u?p-=s.y:"left"===u?p+=s.x:p-=s.x),t[u]=p):t[u]=(d.width-a.width)/2}}catch(m){e={error:m}}finally{try{h&&!h.done&&(i=l.return)&&i.call(l)}finally{if(e)throw e.error}}},e.prototype.maybeRestoreFocus=function(){var t=this,e=this.adapter.isFocused(),i=this.adapter.getOwnerDocument?this.adapter.getOwnerDocument():document,n=i.activeElement&&this.adapter.isElementInContainer(i.activeElement);(e||n)&&setTimeout((function(){t.adapter.restoreFocus()}),s.nL.TOUCH_EVENT_WAIT_MS)},e.prototype.hasBit=function(t,e){return Boolean(t&e)},e.prototype.setBit=function(t,e){return t|e},e.prototype.unsetBit=function(t,e){return t^e},e.prototype.isFinite=function(t){return"number"==typeof t&&isFinite(t)},e}(r.I);const d=a;var c=i(1086),l=i(6584),h=i(6029),u=i(8597),p=i(9760),m=i(2506);const f={TOP_LEFT:s.OK.TOP_LEFT,TOP_RIGHT:s.OK.TOP_RIGHT,BOTTOM_LEFT:s.OK.BOTTOM_LEFT,BOTTOM_RIGHT:s.OK.BOTTOM_RIGHT,TOP_START:s.OK.TOP_START,TOP_END:s.OK.TOP_END,BOTTOM_START:s.OK.BOTTOM_START,BOTTOM_END:s.OK.BOTTOM_END};class g extends c.O{constructor(){super(...arguments),this.mdcFoundationClass=d,this.absolute=!1,this.fullwidth=!1,this.fixed=!1,this.x=null,this.y=null,this.quick=!1,this.open=!1,this.stayOpenOnBodyClick=!1,this.bitwiseCorner=s.OK.TOP_START,this.previousMenuCorner=null,this.menuCorner="START",this.corner="TOP_START",this.styleTop="",this.styleLeft="",this.styleRight="",this.styleBottom="",this.styleMaxHeight="",this.styleTransformOrigin="",this.anchor=null,this.previouslyFocused=null,this.previousAnchor=null,this.onBodyClickBound=()=>{}}render(){return this.renderSurface()}renderSurface(){const t=this.getRootClasses(),e=this.getRootStyles();return u.qy`
      <div
          class=${(0,p.H)(t)}
          style="${(0,m.W)(e)}"
          @keydown=${this.onKeydown}
          @opened=${this.registerBodyClick}
          @closed=${this.deregisterBodyClick}>
        ${this.renderContent()}
      </div>`}getRootClasses(){return{"mdc-menu-surface":!0,"mdc-menu-surface--fixed":this.fixed,"mdc-menu-surface--fullwidth":this.fullwidth}}getRootStyles(){return{top:this.styleTop,left:this.styleLeft,right:this.styleRight,bottom:this.styleBottom,"max-height":this.styleMaxHeight,"transform-origin":this.styleTransformOrigin}}renderContent(){return u.qy`<slot></slot>`}createAdapter(){return Object.assign(Object.assign({},(0,c.i)(this.mdcRoot)),{hasAnchor:()=>!!this.anchor,notifyClose:()=>{const t=new CustomEvent("closed",{bubbles:!0,composed:!0});this.open=!1,this.mdcRoot.dispatchEvent(t)},notifyClosing:()=>{const t=new CustomEvent("closing",{bubbles:!0,composed:!0});this.mdcRoot.dispatchEvent(t)},notifyOpen:()=>{const t=new CustomEvent("opened",{bubbles:!0,composed:!0});this.open=!0,this.mdcRoot.dispatchEvent(t)},notifyOpening:()=>{const t=new CustomEvent("opening",{bubbles:!0,composed:!0});this.mdcRoot.dispatchEvent(t)},isElementInContainer:()=>!1,isRtl:()=>!!this.mdcRoot&&"rtl"===getComputedStyle(this.mdcRoot).direction,setTransformOrigin:t=>{this.mdcRoot&&(this.styleTransformOrigin=t)},isFocused:()=>(0,h.SE)(this),saveFocus:()=>{const t=(0,h.U9)(),e=t.length;e||(this.previouslyFocused=null),this.previouslyFocused=t[e-1]},restoreFocus:()=>{this.previouslyFocused&&"focus"in this.previouslyFocused&&this.previouslyFocused.focus()},getInnerDimensions:()=>{const t=this.mdcRoot;return t?{width:t.offsetWidth,height:t.offsetHeight}:{width:0,height:0}},getAnchorDimensions:()=>{const t=this.anchor;return t?t.getBoundingClientRect():null},getBodyDimensions:()=>({width:document.body.clientWidth,height:document.body.clientHeight}),getWindowDimensions:()=>({width:window.innerWidth,height:window.innerHeight}),getWindowScroll:()=>({x:window.pageXOffset,y:window.pageYOffset}),setPosition:t=>{this.mdcRoot&&(this.styleLeft="left"in t?`${t.left}px`:"",this.styleRight="right"in t?`${t.right}px`:"",this.styleTop="top"in t?`${t.top}px`:"",this.styleBottom="bottom"in t?`${t.bottom}px`:"")},setMaxHeight:async t=>{this.mdcRoot&&(this.styleMaxHeight=t,await this.updateComplete,this.styleMaxHeight=`var(--mdc-menu-max-height, ${t})`)}})}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onBodyClick(t){if(this.stayOpenOnBodyClick)return;-1===t.composedPath().indexOf(this)&&this.close()}registerBodyClick(){this.onBodyClickBound=this.onBodyClick.bind(this),document.body.addEventListener("click",this.onBodyClickBound,{passive:!0,capture:!0})}deregisterBodyClick(){document.body.removeEventListener("click",this.onBodyClickBound,{capture:!0})}onOpenChanged(t,e){this.mdcFoundation&&(t?this.mdcFoundation.open():void 0!==e&&this.mdcFoundation.close())}close(){this.open=!1}show(){this.open=!0}}(0,n.Cg)([(0,o.P)(".mdc-menu-surface")],g.prototype,"mdcRoot",void 0),(0,n.Cg)([(0,o.P)("slot")],g.prototype,"slotElement",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean}),(0,l.P)((function(t){this.mdcFoundation&&!this.fixed&&this.mdcFoundation.setIsHoisted(t)}))],g.prototype,"absolute",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],g.prototype,"fullwidth",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean}),(0,l.P)((function(t){this.mdcFoundation&&!this.absolute&&this.mdcFoundation.setFixedPosition(t)}))],g.prototype,"fixed",void 0),(0,n.Cg)([(0,o.MZ)({type:Number}),(0,l.P)((function(t){this.mdcFoundation&&null!==this.y&&null!==t&&(this.mdcFoundation.setAbsolutePosition(t,this.y),this.mdcFoundation.setAnchorMargin({left:t,top:this.y,right:-t,bottom:this.y}))}))],g.prototype,"x",void 0),(0,n.Cg)([(0,o.MZ)({type:Number}),(0,l.P)((function(t){this.mdcFoundation&&null!==this.x&&null!==t&&(this.mdcFoundation.setAbsolutePosition(this.x,t),this.mdcFoundation.setAnchorMargin({left:this.x,top:t,right:-this.x,bottom:t}))}))],g.prototype,"y",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean}),(0,l.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setQuickOpen(t)}))],g.prototype,"quick",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean,reflect:!0}),(0,l.P)((function(t,e){this.onOpenChanged(t,e)}))],g.prototype,"open",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],g.prototype,"stayOpenOnBodyClick",void 0),(0,n.Cg)([(0,o.wk)(),(0,l.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setAnchorCorner(t)}))],g.prototype,"bitwiseCorner",void 0),(0,n.Cg)([(0,o.MZ)({type:String}),(0,l.P)((function(t){if(this.mdcFoundation){const e="START"===t||"END"===t,i=null===this.previousMenuCorner,n=!i&&t!==this.previousMenuCorner;e&&(n||i&&"END"===t)&&(this.bitwiseCorner=this.bitwiseCorner^s.Jv.RIGHT,this.mdcFoundation.flipCornerHorizontally(),this.previousMenuCorner=t)}}))],g.prototype,"menuCorner",void 0),(0,n.Cg)([(0,o.MZ)({type:String}),(0,l.P)((function(t){if(this.mdcFoundation&&t){let e=f[t];"END"===this.menuCorner&&(e^=s.Jv.RIGHT),this.bitwiseCorner=e}}))],g.prototype,"corner",void 0),(0,n.Cg)([(0,o.wk)()],g.prototype,"styleTop",void 0),(0,n.Cg)([(0,o.wk)()],g.prototype,"styleLeft",void 0),(0,n.Cg)([(0,o.wk)()],g.prototype,"styleRight",void 0),(0,n.Cg)([(0,o.wk)()],g.prototype,"styleBottom",void 0),(0,n.Cg)([(0,o.wk)()],g.prototype,"styleMaxHeight",void 0),(0,n.Cg)([(0,o.wk)()],g.prototype,"styleTransformOrigin",void 0);const y=u.AH`.mdc-menu-surface{display:none;position:absolute;box-sizing:border-box;max-width:calc(100vw - 32px);max-width:var(--mdc-menu-max-width, calc(100vw - 32px));max-height:calc(100vh - 32px);max-height:var(--mdc-menu-max-height, calc(100vh - 32px));margin:0;padding:0;transform:scale(1);transform-origin:top left;opacity:0;overflow:auto;will-change:transform,opacity;z-index:8;transition:opacity .03s linear,transform .12s cubic-bezier(0, 0, 0.2, 1),height 250ms cubic-bezier(0, 0, 0.2, 1);box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12);background-color:#fff;background-color:var(--mdc-theme-surface, #fff);color:#000;color:var(--mdc-theme-on-surface, #000);border-radius:4px;border-radius:var(--mdc-shape-medium, 4px);transform-origin-left:top left;transform-origin-right:top right}.mdc-menu-surface:focus{outline:none}.mdc-menu-surface--animating-open{display:inline-block;transform:scale(0.8);opacity:0}.mdc-menu-surface--open{display:inline-block;transform:scale(1);opacity:1}.mdc-menu-surface--animating-closed{display:inline-block;opacity:0;transition:opacity .075s linear}[dir=rtl] .mdc-menu-surface,.mdc-menu-surface[dir=rtl]{transform-origin-left:top right;transform-origin-right:top left}.mdc-menu-surface--anchor{position:relative;overflow:visible}.mdc-menu-surface--fixed{position:fixed}.mdc-menu-surface--fullwidth{width:100%}:host(:not([open])){display:none}.mdc-menu-surface{z-index:8;z-index:var(--mdc-menu-z-index, 8);min-width:112px;min-width:var(--mdc-menu-min-width, 112px)}`;let T=class extends g{};T.styles=[y],T=(0,n.Cg)([(0,o.EM)("mwc-menu-surface")],T);var O,C={MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"},b={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list,.mdc-deprecated-list",SELECTED_EVENT:"MDCMenu:selected",SKIP_RESTORE_FOCUS:"data-menu-item-skip-restore-focus"},E={FOCUS_ROOT_INDEX:-1};!function(t){t[t.NONE=0]="NONE",t[t.LIST_ROOT=1]="LIST_ROOT",t[t.FIRST_ITEM=2]="FIRST_ITEM",t[t.LAST_ITEM=3]="LAST_ITEM"}(O||(O={}));var v=i(852);const I=function(t){function e(i){var o=t.call(this,(0,n.Cl)((0,n.Cl)({},e.defaultAdapter),i))||this;return o.closeAnimationEndTimerId=0,o.defaultFocusState=O.LIST_ROOT,o.selectedIndex=-1,o}return(0,n.C6)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return C},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return b},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return E},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},getAttributeFromElementAtIndex:function(){return null},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!1,configurable:!0}),e.prototype.destroy=function(){this.closeAnimationEndTimerId&&clearTimeout(this.closeAnimationEndTimerId),this.adapter.closeSurface()},e.prototype.handleKeydown=function(t){var e=t.key,i=t.keyCode;("Tab"===e||9===i)&&this.adapter.closeSurface(!0)},e.prototype.handleItemAction=function(t){var e=this,i=this.adapter.getElementIndex(t);if(!(i<0)){this.adapter.notifySelected({index:i});var n="true"===this.adapter.getAttributeFromElementAtIndex(i,b.SKIP_RESTORE_FOCUS);this.adapter.closeSurface(n),this.closeAnimationEndTimerId=setTimeout((function(){var i=e.adapter.getElementIndex(t);i>=0&&e.adapter.isSelectableItemAtIndex(i)&&e.setSelectedIndex(i)}),a.numbers.TRANSITION_CLOSE_DURATION)}},e.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState){case O.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case O.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case O.NONE:break;default:this.adapter.focusListRoot()}},e.prototype.setDefaultFocusState=function(t){this.defaultFocusState=t},e.prototype.getSelectedIndex=function(){return this.selectedIndex},e.prototype.setSelectedIndex=function(t){if(this.validatedIndex(t),!this.adapter.isSelectableItemAtIndex(t))throw new Error("MDCMenuFoundation: No selection group at specified index.");var e=this.adapter.getSelectedSiblingOfItemAtIndex(t);e>=0&&(this.adapter.removeAttributeFromElementAtIndex(e,b.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(e,C.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(t,C.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(t,b.ARIA_CHECKED_ATTR,"true"),this.selectedIndex=t},e.prototype.setEnabled=function(t,e){this.validatedIndex(t),e?(this.adapter.removeClassFromElementAtIndex(t,v.Y7.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(t,b.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(t,v.Y7.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(t,b.ARIA_DISABLED_ATTR,"true"))},e.prototype.validatedIndex=function(t){var e=this.adapter.getMenuItemCount();if(!(t>=0&&t<e))throw new Error("MDCMenuFoundation: No list item at specified index.")},e}(r.I);i(9335);class x extends c.O{constructor(){super(...arguments),this.mdcFoundationClass=I,this.listElement_=null,this.anchor=null,this.open=!1,this.quick=!1,this.wrapFocus=!1,this.innerRole="menu",this.innerAriaLabel=null,this.corner="TOP_START",this.x=null,this.y=null,this.absolute=!1,this.multi=!1,this.activatable=!1,this.fixed=!1,this.forceGroupSelection=!1,this.fullwidth=!1,this.menuCorner="START",this.stayOpenOnBodyClick=!1,this.defaultFocus="LIST_ROOT",this._listUpdateComplete=null}get listElement(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}get items(){const t=this.listElement;return t?t.items:[]}get index(){const t=this.listElement;return t?t.index:-1}get selected(){const t=this.listElement;return t?t.selected:null}render(){return this.renderSurface()}renderSurface(){const t=this.getSurfaceClasses();return u.qy`
      <mwc-menu-surface
        ?hidden=${!this.open}
        .anchor=${this.anchor}
        .open=${this.open}
        .quick=${this.quick}
        .corner=${this.corner}
        .x=${this.x}
        .y=${this.y}
        .absolute=${this.absolute}
        .fixed=${this.fixed}
        .fullwidth=${this.fullwidth}
        .menuCorner=${this.menuCorner}
        ?stayOpenOnBodyClick=${this.stayOpenOnBodyClick}
        class=${(0,p.H)(t)}
        @closed=${this.onClosed}
        @opened=${this.onOpened}
        @keydown=${this.onKeydown}>
      ${this.renderList()}
    </mwc-menu-surface>`}getSurfaceClasses(){return{"mdc-menu":!0,"mdc-menu-surface":!0}}renderList(){const t="menu"===this.innerRole?"menuitem":"option",e=this.renderListClasses();return u.qy`
      <mwc-list
          rootTabbable
          .innerAriaLabel=${this.innerAriaLabel}
          .innerRole=${this.innerRole}
          .multi=${this.multi}
          class=${(0,p.H)(e)}
          .itemRoles=${t}
          .wrapFocus=${this.wrapFocus}
          .activatable=${this.activatable}
          @action=${this.onAction}>
        <slot></slot>
      </mwc-list>`}renderListClasses(){return{"mdc-deprecated-list":!0}}createAdapter(){return{addClassToElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&("mdc-menu-item--selected"===e?this.forceGroupSelection&&!n.selected&&i.toggle(t,!0):n.classList.add(e))},removeClassFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&("mdc-menu-item--selected"===e?n.selected&&i.toggle(t,!1):n.classList.remove(e))},addAttributeToElementAtIndex:(t,e,i)=>{const n=this.listElement;if(!n)return;const o=n.items[t];o&&o.setAttribute(e,i)},removeAttributeFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&n.removeAttribute(e)},getAttributeFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return null;const n=i.items[t];return n?n.getAttribute(e):null},elementContainsClass:(t,e)=>t.classList.contains(e),closeSurface:()=>{this.open=!1},getElementIndex:t=>{const e=this.listElement;return e?e.items.indexOf(t):-1},notifySelected:()=>{},getMenuItemCount:()=>{const t=this.listElement;return t?t.items.length:0},focusItemAtIndex:t=>{const e=this.listElement;if(!e)return;const i=e.items[t];i&&i.focus()},focusListRoot:()=>{this.listElement&&this.listElement.focus()},getSelectedSiblingOfItemAtIndex:t=>{const e=this.listElement;if(!e)return-1;const i=e.items[t];if(!i||!i.group)return-1;for(let n=0;n<e.items.length;n++){if(n===t)continue;const o=e.items[n];if(o.selected&&o.group===i.group)return n}return-1},isSelectableItemAtIndex:t=>{const e=this.listElement;if(!e)return!1;const i=e.items[t];return!!i&&i.hasAttribute("group")}}}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onAction(t){const e=this.listElement;if(this.mdcFoundation&&e){const i=t.detail.index,n=e.items[i];n&&this.mdcFoundation.handleItemAction(n)}}onOpened(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}onClosed(){this.open=!1}async getUpdateComplete(){await this._listUpdateComplete;return await super.getUpdateComplete()}async firstUpdated(){super.firstUpdated();const t=this.listElement;t&&(this._listUpdateComplete=t.updateComplete,await this._listUpdateComplete)}select(t){const e=this.listElement;e&&e.select(t)}close(){this.open=!1}show(){this.open=!0}getFocusedItemIndex(){const t=this.listElement;return t?t.getFocusedItemIndex():-1}focusItemAtIndex(t){const e=this.listElement;e&&e.focusItemAtIndex(t)}layout(t=!0){const e=this.listElement;e&&e.layout(t)}}(0,n.Cg)([(0,o.P)(".mdc-menu")],x.prototype,"mdcRoot",void 0),(0,n.Cg)([(0,o.P)("slot")],x.prototype,"slotElement",void 0),(0,n.Cg)([(0,o.MZ)({type:Object})],x.prototype,"anchor",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean,reflect:!0})],x.prototype,"open",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"quick",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"wrapFocus",void 0),(0,n.Cg)([(0,o.MZ)({type:String})],x.prototype,"innerRole",void 0),(0,n.Cg)([(0,o.MZ)({type:String})],x.prototype,"innerAriaLabel",void 0),(0,n.Cg)([(0,o.MZ)({type:String})],x.prototype,"corner",void 0),(0,n.Cg)([(0,o.MZ)({type:Number})],x.prototype,"x",void 0),(0,n.Cg)([(0,o.MZ)({type:Number})],x.prototype,"y",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"absolute",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"multi",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"activatable",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"fixed",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"forceGroupSelection",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"fullwidth",void 0),(0,n.Cg)([(0,o.MZ)({type:String})],x.prototype,"menuCorner",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],x.prototype,"stayOpenOnBodyClick",void 0),(0,n.Cg)([(0,o.MZ)({type:String}),(0,l.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(O[t])}))],x.prototype,"defaultFocus",void 0);const A=u.AH`mwc-list ::slotted([mwc-list-item]:not([twoline])),mwc-list ::slotted([noninteractive]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}`;let S=class extends x{};S.styles=[A],S=(0,n.Cg)([(0,o.EM)("mwc-menu")],S)}};
//# sourceMappingURL=GLI4E-_4.js.map