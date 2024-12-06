import { g as Ne, b as Fe } from "./Index-DTcMbqJo.js";
const y = window.ms_globals.React, Ae = window.ms_globals.React.forwardRef, Le = window.ms_globals.React.useRef, Ke = window.ms_globals.React.useState, Me = window.ms_globals.React.useEffect, qe = window.ms_globals.ReactDOM.createPortal;
function Be(e) {
  return e === void 0;
}
function k() {
}
function Te(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function ze(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return k;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function P(e) {
  let t;
  return ze(e, (n) => t = n)(), t;
}
const w = [];
function b(e, t = k) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function s(c) {
    if (Te(e, c) && (e = c, n)) {
      const u = !w.length;
      for (const a of r)
        a[1](), w.push(a, e);
      if (u) {
        for (let a = 0; a < w.length; a += 2)
          w[a][0](w[a + 1]);
        w.length = 0;
      }
    }
  }
  function o(c) {
    s(c(e));
  }
  function i(c, u = k) {
    const a = [c, u];
    return r.add(a), r.size === 1 && (n = t(s, o) || k), c(e), () => {
      r.delete(a), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: s,
    update: o,
    subscribe: i
  };
}
const {
  getContext: U,
  setContext: I
} = window.__gradio__svelte__internal, De = "$$ms-gr-slots-key";
function Ue() {
  const e = b({});
  return I(De, e);
}
const We = "$$ms-gr-render-slot-context-key";
function Ge() {
  const e = I(We, b({}));
  return (t, n) => {
    e.update((r) => typeof n == "function" ? {
      ...r,
      [t]: n(r[t])
    } : {
      ...r,
      [t]: n
    });
  };
}
const He = "$$ms-gr-context-key";
function L(e) {
  return Be(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const Ie = "$$ms-gr-sub-index-context-key";
function Je() {
  return U(Ie) || null;
}
function he(e) {
  return I(Ie, e);
}
function Ye(e, t, n) {
  var g, m;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = Ee(), s = Ze({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), o = Je();
  typeof o == "number" && he(void 0), typeof e._internal.subIndex == "number" && he(e._internal.subIndex), r && r.subscribe((l) => {
    s.slotKey.set(l);
  }), Qe();
  const i = U(He), c = ((g = P(i)) == null ? void 0 : g.as_item) || e.as_item, u = L(i ? c ? ((m = P(i)) == null ? void 0 : m[c]) || {} : P(i) || {} : {}), a = (l, p) => l ? Ne({
    ...l,
    ...p || {}
  }, t) : void 0, f = b({
    ...e,
    _internal: {
      ...e._internal,
      index: o ?? e._internal.index
    },
    ...u,
    restProps: a(e.restProps, u),
    originalRestProps: e.restProps
  });
  return i ? (i.subscribe((l) => {
    const {
      as_item: p
    } = P(f);
    p && (l = l == null ? void 0 : l[p]), l = L(l), f.update((_) => ({
      ..._,
      ...l || {},
      restProps: a(_.restProps, l)
    }));
  }), [f, (l) => {
    var _;
    const p = L(l.as_item ? ((_ = P(i)) == null ? void 0 : _[l.as_item]) || {} : P(i) || {});
    return f.set({
      ...l,
      _internal: {
        ...l._internal,
        index: o ?? l._internal.index
      },
      ...p,
      restProps: a(l.restProps, p),
      originalRestProps: l.restProps
    });
  }]) : [f, (l) => {
    f.set({
      ...l,
      _internal: {
        ...l._internal,
        index: o ?? l._internal.index
      },
      restProps: a(l.restProps),
      originalRestProps: l.restProps
    });
  }];
}
const Ce = "$$ms-gr-slot-key";
function Qe() {
  I(Ce, b(void 0));
}
function Ee() {
  return U(Ce);
}
const Xe = "$$ms-gr-component-slot-context-key";
function Ze({
  slot: e,
  index: t,
  subIndex: n
}) {
  return I(Xe, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(n)
  });
}
function Ve(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function $e(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Se = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var et = y, tt = Symbol.for("react.element"), nt = Symbol.for("react.fragment"), rt = Object.prototype.hasOwnProperty, ot = et.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, st = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Re(e, t, n) {
  var r, s = {}, o = null, i = null;
  n !== void 0 && (o = "" + n), t.key !== void 0 && (o = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (r in t) rt.call(t, r) && !st.hasOwnProperty(r) && (s[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) s[r] === void 0 && (s[r] = t[r]);
  return {
    $$typeof: tt,
    type: e,
    key: o,
    ref: i,
    props: s,
    _owner: ot.current
  };
}
F.Fragment = nt;
F.jsx = Re;
F.jsxs = Re;
Se.exports = F;
var M = Se.exports;
const it = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function lt(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return typeof r == "number" && !it.includes(n) ? t[n] = r + "px" : t[n] = r, t;
  }, {}) : {};
}
function q(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(qe(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: y.Children.toArray(e._reactElement.props.children).map((s) => {
        if (y.isValidElement(s) && s.props.__slot__) {
          const {
            portals: o,
            clonedElement: i
          } = q(s.props.el);
          return y.cloneElement(s, {
            ...s.props,
            el: i,
            children: [...y.Children.toArray(s.props.children), ...o]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((s) => {
    e.getEventListeners(s).forEach(({
      listener: i,
      type: c,
      useCapture: u
    }) => {
      n.addEventListener(c, i, u);
    });
  });
  const r = Array.from(e.childNodes);
  for (let s = 0; s < r.length; s++) {
    const o = r[s];
    if (o.nodeType === 1) {
      const {
        clonedElement: i,
        portals: c
      } = q(o);
      t.push(...c), n.appendChild(i);
    } else o.nodeType === 3 && n.appendChild(o.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function ct(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const B = Ae(({
  slot: e,
  clone: t,
  className: n,
  style: r
}, s) => {
  const o = Le(), [i, c] = Ke([]);
  return Me(() => {
    var g;
    if (!o.current || !e)
      return;
    let u = e;
    function a() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), ct(s, m), n && m.classList.add(...n.split(" ")), r) {
        const l = lt(r);
        Object.keys(l).forEach((p) => {
          m.style[p] = l[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let m = function() {
        var _;
        const {
          portals: l,
          clonedElement: p
        } = q(e);
        u = p, c(l), u.style.display = "contents", a(), (_ = o.current) == null || _.appendChild(u);
      };
      m(), f = new window.MutationObserver(() => {
        var l, p;
        (l = o.current) != null && l.contains(u) && ((p = o.current) == null || p.removeChild(u)), m();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", a(), (g = o.current) == null || g.appendChild(u);
    return () => {
      var m, l;
      u.style.display = "", (m = o.current) != null && m.contains(u) && ((l = o.current) == null || l.removeChild(u)), f == null || f.disconnect();
    };
  }, [e, t, n, r, s]), y.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...i);
});
function T(e, t) {
  return e.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return t != null && t.fallback ? t.fallback(n) : n;
    const r = {
      ...n.props
    };
    let s = r;
    Object.keys(n.slots).forEach((i) => {
      if (!n.slots[i] || !(n.slots[i] instanceof Element) && !n.slots[i].el)
        return;
      const c = i.split(".");
      c.forEach((m, l) => {
        s[m] || (s[m] = {}), l !== c.length - 1 && (s = r[m]);
      });
      const u = n.slots[i];
      let a, f, g = (t == null ? void 0 : t.clone) ?? !1;
      u instanceof Element ? a = u : (a = u.el, f = u.callback, g = u.clone ?? !1), s[c[c.length - 1]] = a ? f ? (...m) => (f(c[c.length - 1], m), /* @__PURE__ */ M.jsx(B, {
        slot: a,
        clone: g
      })) : /* @__PURE__ */ M.jsx(B, {
        slot: a,
        clone: g
      }) : s[c[c.length - 1]], s = r;
    });
    const o = (t == null ? void 0 : t.children) || "children";
    return n[o] && (r[o] = T(n[o], t)), r;
  });
}
function z(e, t) {
  return e ? /* @__PURE__ */ M.jsx(B, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function K({
  key: e,
  setSlotParams: t,
  slots: n
}, r) {
  return n[e] ? (...s) => (t(e, s), z(n[e], {
    clone: !0,
    ...r
  })) : void 0;
}
var Oe = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function n() {
      for (var o = "", i = 0; i < arguments.length; i++) {
        var c = arguments[i];
        c && (o = s(o, r(c)));
      }
      return o;
    }
    function r(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return n.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var i = "";
      for (var c in o)
        t.call(o, c) && o[c] && (i = s(i, c));
      return i;
    }
    function s(o, i) {
      return i ? o ? o + " " + i : o + i : o;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(Oe);
var ut = Oe.exports;
const dt = /* @__PURE__ */ $e(ut), {
  getContext: at,
  setContext: ft
} = window.__gradio__svelte__internal;
function ve(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(s = ["default"]) {
    const o = s.reduce((i, c) => (i[c] = b([]), i), {});
    return ft(t, {
      itemsMap: o,
      allowedSlots: s
    }), o;
  }
  function r() {
    const {
      itemsMap: s,
      allowedSlots: o
    } = at(t);
    return function(i, c, u) {
      s && (i ? s[i].update((a) => {
        const f = [...a];
        return o.includes(i) ? f[c] = u : f[c] = void 0, f;
      }) : o.includes("default") && s.default.update((a) => {
        const f = [...a];
        return f[c] = u, f;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: r
  };
}
const {
  getItems: mt,
  getSetItemFn: jt
} = ve("menu"), {
  getItems: kt,
  getSetItemFn: pt
} = ve("breadcrumb"), {
  SvelteComponent: _t,
  assign: ye,
  check_outros: gt,
  component_subscribe: x,
  compute_rest_props: Pe,
  create_slot: bt,
  detach: ht,
  empty: we,
  exclude_internal_props: yt,
  flush: h,
  get_all_dirty_from_scope: Pt,
  get_slot_changes: wt,
  group_outros: xt,
  init: It,
  insert_hydration: Ct,
  safe_not_equal: Et,
  transition_in: N,
  transition_out: D,
  update_slot_base: St
} = window.__gradio__svelte__internal;
function xe(e) {
  let t;
  const n = (
    /*#slots*/
    e[21].default
  ), r = bt(
    n,
    e,
    /*$$scope*/
    e[20],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(s) {
      r && r.l(s);
    },
    m(s, o) {
      r && r.m(s, o), t = !0;
    },
    p(s, o) {
      r && r.p && (!t || o & /*$$scope*/
      1048576) && St(
        r,
        n,
        s,
        /*$$scope*/
        s[20],
        t ? wt(
          n,
          /*$$scope*/
          s[20],
          o,
          null
        ) : Pt(
          /*$$scope*/
          s[20]
        ),
        null
      );
    },
    i(s) {
      t || (N(r, s), t = !0);
    },
    o(s) {
      D(r, s), t = !1;
    },
    d(s) {
      r && r.d(s);
    }
  };
}
function Rt(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[0].visible && xe(e)
  );
  return {
    c() {
      r && r.c(), t = we();
    },
    l(s) {
      r && r.l(s), t = we();
    },
    m(s, o) {
      r && r.m(s, o), Ct(s, t, o), n = !0;
    },
    p(s, [o]) {
      /*$mergedProps*/
      s[0].visible ? r ? (r.p(s, o), o & /*$mergedProps*/
      1 && N(r, 1)) : (r = xe(s), r.c(), N(r, 1), r.m(t.parentNode, t)) : r && (xt(), D(r, 1, 1, () => {
        r = null;
      }), gt());
    },
    i(s) {
      n || (N(r), n = !0);
    },
    o(s) {
      D(r), n = !1;
    },
    d(s) {
      s && ht(t), r && r.d(s);
    }
  };
}
function Ot(e, t, n) {
  const r = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let s = Pe(t, r), o, i, c, u, a, f, {
    $$slots: g = {},
    $$scope: m
  } = t, {
    gradio: l
  } = t, {
    props: p = {}
  } = t;
  const _ = b(p);
  x(e, _, (d) => n(19, f = d));
  let {
    _internal: C = {}
  } = t, {
    as_item: E
  } = t, {
    visible: S = !0
  } = t, {
    elem_id: R = ""
  } = t, {
    elem_classes: O = []
  } = t, {
    elem_style: v = {}
  } = t;
  const W = Ee();
  x(e, W, (d) => n(16, c = d));
  const [G, je] = Ye({
    gradio: l,
    props: f,
    _internal: C,
    visible: S,
    elem_id: R,
    elem_classes: O,
    elem_style: v,
    as_item: E,
    restProps: s
  });
  x(e, G, (d) => n(0, i = d));
  const H = Ue();
  x(e, H, (d) => n(15, o = d));
  const ke = pt(), A = Ge(), {
    "menu.items": J,
    "dropdownProps.menu.items": Y
  } = mt(["menu.items", "dropdownProps.menu.items"]);
  return x(e, J, (d) => n(18, a = d)), x(e, Y, (d) => n(17, u = d)), e.$$set = (d) => {
    t = ye(ye({}, t), yt(d)), n(25, s = Pe(t, r)), "gradio" in d && n(7, l = d.gradio), "props" in d && n(8, p = d.props), "_internal" in d && n(9, C = d._internal), "as_item" in d && n(10, E = d.as_item), "visible" in d && n(11, S = d.visible), "elem_id" in d && n(12, R = d.elem_id), "elem_classes" in d && n(13, O = d.elem_classes), "elem_style" in d && n(14, v = d.elem_style), "$$scope" in d && n(20, m = d.$$scope);
  }, e.$$.update = () => {
    var d, Q, X, Z, V, $, ee, te, ne, re, oe, se, ie, le, ce, ue, de, ae, fe, me, pe, _e;
    if (e.$$.dirty & /*props*/
    256 && _.update((j) => ({
      ...j,
      ...p
    })), je({
      gradio: l,
      props: f,
      _internal: C,
      visible: S,
      elem_id: R,
      elem_classes: O,
      elem_style: v,
      as_item: E,
      restProps: s
    }), e.$$.dirty & /*$mergedProps, $menuItems, $slots, $dropdownMenuItems, $slotKey*/
    491521) {
      const j = {
        ...i.restProps.menu || {},
        ...i.props.menu || {},
        items: (d = i.props.menu) != null && d.items || (Q = i.restProps.menu) != null && Q.items || a.length > 0 ? T(a, {
          clone: !0
        }) : void 0,
        expandIcon: K({
          setSlotParams: A,
          slots: o,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) || ((X = i.props.menu) == null ? void 0 : X.expandIcon) || ((Z = i.restProps.menu) == null ? void 0 : Z.expandIcon),
        overflowedIndicator: z(o["menu.overflowedIndicator"]) || ((V = i.props.menu) == null ? void 0 : V.overflowedIndicator) || (($ = i.restProps.menu) == null ? void 0 : $.overflowedIndicator)
      }, ge = {
        ...((ee = i.restProps.dropdownProps) == null ? void 0 : ee.menu) || {},
        ...((te = i.props.dropdownProps) == null ? void 0 : te.menu) || {},
        items: (re = (ne = i.props.dropdownProps) == null ? void 0 : ne.menu) != null && re.items || (se = (oe = i.restProps.dropdownProps) == null ? void 0 : oe.menu) != null && se.items || u.length > 0 ? T(u, {
          clone: !0
        }) : void 0,
        expandIcon: K({
          setSlotParams: A,
          slots: o,
          key: "dropdownProps.menu.expandIcon"
        }, {
          clone: !0
        }) || ((le = (ie = i.props.dropdownProps) == null ? void 0 : ie.menu) == null ? void 0 : le.expandIcon) || ((ue = (ce = i.restProps.dropdownProps) == null ? void 0 : ce.menu) == null ? void 0 : ue.expandIcon),
        overflowedIndicator: z(o["dropdownProps.menu.overflowedIndicator"]) || ((ae = (de = i.props.dropdownProps) == null ? void 0 : de.menu) == null ? void 0 : ae.overflowedIndicator) || ((me = (fe = i.restProps.dropdownProps) == null ? void 0 : fe.menu) == null ? void 0 : me.overflowedIndicator)
      }, be = {
        ...i.restProps.dropdownProps || {},
        ...i.props.dropdownProps || {},
        dropdownRender: o["dropdownProps.dropdownRender"] ? K({
          setSlotParams: A,
          slots: o,
          key: "dropdownProps.dropdownRender"
        }, {
          clone: !0
        }) : Ve(((pe = i.props.dropdownProps) == null ? void 0 : pe.dropdownRender) || ((_e = i.restProps.dropdownProps) == null ? void 0 : _e.dropdownRender)),
        menu: Object.values(ge).filter(Boolean).length > 0 ? ge : void 0
      };
      ke(c, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: dt(i.elem_classes, "ms-gr-antd-breadcrumb-item"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...Fe(i),
          menu: Object.values(j).filter(Boolean).length > 0 ? j : void 0,
          dropdownProps: Object.values(be).filter(Boolean).length > 0 ? be : void 0
        },
        slots: {
          title: o.title
        }
      });
    }
  }, [i, _, W, G, H, J, Y, l, p, C, E, S, R, O, v, o, c, u, a, f, m, g];
}
class Nt extends _t {
  constructor(t) {
    super(), It(this, t, Ot, Rt, Et, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), h();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), h();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), h();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), h();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), h();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), h();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), h();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), h();
  }
}
export {
  Nt as default
};
