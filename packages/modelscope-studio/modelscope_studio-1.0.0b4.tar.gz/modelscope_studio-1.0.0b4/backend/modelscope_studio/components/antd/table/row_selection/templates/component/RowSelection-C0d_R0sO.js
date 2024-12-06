import { g as oe, b as ie } from "./Index-CrFfRUIm.js";
const y = window.ms_globals.React, le = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, ae = window.ms_globals.React.useEffect, fe = window.ms_globals.ReactDOM.createPortal;
function de(e) {
  return e === void 0;
}
function k() {
}
function me(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function _e(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return k;
  }
  const s = e.subscribe(...t);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function x(e) {
  let t;
  return _e(e, (s) => t = s)(), t;
}
const C = [];
function b(e, t = k) {
  let s;
  const n = /* @__PURE__ */ new Set();
  function o(c) {
    if (me(e, c) && (e = c, s)) {
      const u = !C.length;
      for (const a of n)
        a[1](), C.push(a, e);
      if (u) {
        for (let a = 0; a < C.length; a += 2)
          C[a][0](C[a + 1]);
        C.length = 0;
      }
    }
  }
  function r(c) {
    o(c(e));
  }
  function i(c, u = k) {
    const a = [c, u];
    return n.add(a), n.size === 1 && (s = t(o, r) || k), c(e), () => {
      n.delete(a), n.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: o,
    update: r,
    subscribe: i
  };
}
const {
  getContext: L,
  setContext: S
} = window.__gradio__svelte__internal, pe = "$$ms-gr-slots-key";
function ge() {
  const e = b({});
  return S(pe, e);
}
const be = "$$ms-gr-render-slot-context-key";
function he() {
  const e = S(be, b({}));
  return (t, s) => {
    e.update((n) => typeof s == "function" ? {
      ...n,
      [t]: s(n[t])
    } : {
      ...n,
      [t]: s
    });
  };
}
const ye = "$$ms-gr-context-key";
function F(e) {
  return de(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const Q = "$$ms-gr-sub-index-context-key";
function xe() {
  return L(Q) || null;
}
function U(e) {
  return S(Q, e);
}
function Ce(e, t, s) {
  var g, d;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = Z(), o = Ee({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), r = xe();
  typeof r == "number" && U(void 0), typeof e._internal.subIndex == "number" && U(e._internal.subIndex), n && n.subscribe((l) => {
    o.slotKey.set(l);
  }), Pe();
  const i = L(ye), c = ((g = x(i)) == null ? void 0 : g.as_item) || e.as_item, u = F(i ? c ? ((d = x(i)) == null ? void 0 : d[c]) || {} : x(i) || {} : {}), a = (l, _) => l ? oe({
    ...l,
    ..._ || {}
  }, t) : void 0, m = b({
    ...e,
    _internal: {
      ...e._internal,
      index: r ?? e._internal.index
    },
    ...u,
    restProps: a(e.restProps, u),
    originalRestProps: e.restProps
  });
  return i ? (i.subscribe((l) => {
    const {
      as_item: _
    } = x(m);
    _ && (l = l == null ? void 0 : l[_]), l = F(l), m.update((p) => ({
      ...p,
      ...l || {},
      restProps: a(p.restProps, l)
    }));
  }), [m, (l) => {
    var p;
    const _ = F(l.as_item ? ((p = x(i)) == null ? void 0 : p[l.as_item]) || {} : x(i) || {});
    return m.set({
      ...l,
      _internal: {
        ...l._internal,
        index: r ?? l._internal.index
      },
      ..._,
      restProps: a(l.restProps, _),
      originalRestProps: l.restProps
    });
  }]) : [m, (l) => {
    m.set({
      ...l,
      _internal: {
        ...l._internal,
        index: r ?? l._internal.index
      },
      restProps: a(l.restProps),
      originalRestProps: l.restProps
    });
  }];
}
const X = "$$ms-gr-slot-key";
function Pe() {
  S(X, b(void 0));
}
function Z() {
  return L(X);
}
const Se = "$$ms-gr-component-slot-context-key";
function Ee({
  slot: e,
  index: t,
  subIndex: s
}) {
  return S(Se, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(s)
  });
}
function N(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function we(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var V = {
  exports: {}
}, v = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ie = y, Re = Symbol.for("react.element"), Oe = Symbol.for("react.fragment"), ke = Object.prototype.hasOwnProperty, je = Ie.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ve = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(e, t, s) {
  var n, o = {}, r = null, i = null;
  s !== void 0 && (r = "" + s), t.key !== void 0 && (r = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (n in t) ke.call(t, n) && !ve.hasOwnProperty(n) && (o[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: Re,
    type: e,
    key: r,
    ref: i,
    props: o,
    _owner: je.current
  };
}
v.Fragment = Oe;
v.jsx = $;
v.jsxs = $;
V.exports = v;
var W = V.exports;
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ne(e) {
  return e ? Object.keys(e).reduce((t, s) => {
    const n = e[s];
    return typeof n == "number" && !Fe.includes(s) ? t[s] = n + "px" : t[s] = n, t;
  }, {}) : {};
}
function T(e) {
  const t = [], s = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(fe(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: y.Children.toArray(e._reactElement.props.children).map((o) => {
        if (y.isValidElement(o) && o.props.__slot__) {
          const {
            portals: r,
            clonedElement: i
          } = T(o.props.el);
          return y.cloneElement(o, {
            ...o.props,
            el: i,
            children: [...y.Children.toArray(o.props.children), ...r]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: i,
      type: c,
      useCapture: u
    }) => {
      s.addEventListener(c, i, u);
    });
  });
  const n = Array.from(e.childNodes);
  for (let o = 0; o < n.length; o++) {
    const r = n[o];
    if (r.nodeType === 1) {
      const {
        clonedElement: i,
        portals: c
      } = T(r);
      t.push(...c), s.appendChild(i);
    } else r.nodeType === 3 && s.appendChild(r.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function Te(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const G = le(({
  slot: e,
  clone: t,
  className: s,
  style: n
}, o) => {
  const r = ce(), [i, c] = ue([]);
  return ae(() => {
    var g;
    if (!r.current || !e)
      return;
    let u = e;
    function a() {
      let d = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (d = u.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Te(o, d), s && d.classList.add(...s.split(" ")), n) {
        const l = Ne(n);
        Object.keys(l).forEach((_) => {
          d.style[_] = l[_];
        });
      }
    }
    let m = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var p;
        const {
          portals: l,
          clonedElement: _
        } = T(e);
        u = _, c(l), u.style.display = "contents", a(), (p = r.current) == null || p.appendChild(u);
      };
      d(), m = new window.MutationObserver(() => {
        var l, _;
        (l = r.current) != null && l.contains(u) && ((_ = r.current) == null || _.removeChild(u)), d();
      }), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", a(), (g = r.current) == null || g.appendChild(u);
    return () => {
      var d, l;
      u.style.display = "", (d = r.current) != null && d.contains(u) && ((l = r.current) == null || l.removeChild(u)), m == null || m.disconnect();
    };
  }, [e, t, s, n, o]), y.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...i);
});
function ee(e, t) {
  return e.filter(Boolean).map((s) => {
    if (typeof s != "object")
      return s;
    const n = {
      ...s.props
    };
    let o = n;
    Object.keys(s.slots).forEach((i) => {
      if (!s.slots[i] || !(s.slots[i] instanceof Element) && !s.slots[i].el)
        return;
      const c = i.split(".");
      c.forEach((d, l) => {
        o[d] || (o[d] = {}), l !== c.length - 1 && (o = n[d]);
      });
      const u = s.slots[i];
      let a, m, g = !1;
      u instanceof Element ? a = u : (a = u.el, m = u.callback, g = u.clone ?? !1), o[c[c.length - 1]] = a ? m ? (...d) => (m(c[c.length - 1], d), /* @__PURE__ */ W.jsx(G, {
        slot: a,
        clone: g
      })) : /* @__PURE__ */ W.jsx(G, {
        slot: a,
        clone: g
      }) : o[c[c.length - 1]], o = n;
    });
    const r = "children";
    return s[r] && (n[r] = ee(s[r])), n;
  });
}
var te = {
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
    function s() {
      for (var r = "", i = 0; i < arguments.length; i++) {
        var c = arguments[i];
        c && (r = o(r, n(c)));
      }
      return r;
    }
    function n(r) {
      if (typeof r == "string" || typeof r == "number")
        return r;
      if (typeof r != "object")
        return "";
      if (Array.isArray(r))
        return s.apply(null, r);
      if (r.toString !== Object.prototype.toString && !r.toString.toString().includes("[native code]"))
        return r.toString();
      var i = "";
      for (var c in r)
        t.call(r, c) && r[c] && (i = o(i, c));
      return i;
    }
    function o(r, i) {
      return i ? r ? r + " " + i : r + i : r;
    }
    e.exports ? (s.default = s, e.exports = s) : window.classNames = s;
  })();
})(te);
var Ae = te.exports;
const Le = /* @__PURE__ */ we(Ae), {
  getContext: Ke,
  setContext: qe
} = window.__gradio__svelte__internal;
function ne(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function s(o = ["default"]) {
    const r = o.reduce((i, c) => (i[c] = b([]), i), {});
    return qe(t, {
      itemsMap: r,
      allowedSlots: o
    }), r;
  }
  function n() {
    const {
      itemsMap: o,
      allowedSlots: r
    } = Ke(t);
    return function(i, c, u) {
      o && (i ? o[i].update((a) => {
        const m = [...a];
        return r.includes(i) ? m[c] = u : m[c] = void 0, m;
      }) : r.includes("default") && o.default.update((a) => {
        const m = [...a];
        return m[c] = u, m;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: n
  };
}
const {
  getItems: Me,
  getSetItemFn: nt
} = ne("table-row-selection-selection"), {
  getItems: st,
  getSetItemFn: ze
} = ne("table-row-selection"), {
  SvelteComponent: De,
  assign: H,
  check_outros: Ue,
  component_subscribe: P,
  compute_rest_props: B,
  create_slot: We,
  detach: Ge,
  empty: J,
  exclude_internal_props: He,
  flush: h,
  get_all_dirty_from_scope: Be,
  get_slot_changes: Je,
  group_outros: Ye,
  init: Qe,
  insert_hydration: Xe,
  safe_not_equal: Ze,
  transition_in: j,
  transition_out: A,
  update_slot_base: Ve
} = window.__gradio__svelte__internal;
function Y(e) {
  let t;
  const s = (
    /*#slots*/
    e[19].default
  ), n = We(
    s,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    l(o) {
      n && n.l(o);
    },
    m(o, r) {
      n && n.m(o, r), t = !0;
    },
    p(o, r) {
      n && n.p && (!t || r & /*$$scope*/
      262144) && Ve(
        n,
        s,
        o,
        /*$$scope*/
        o[18],
        t ? Je(
          s,
          /*$$scope*/
          o[18],
          r,
          null
        ) : Be(
          /*$$scope*/
          o[18]
        ),
        null
      );
    },
    i(o) {
      t || (j(n, o), t = !0);
    },
    o(o) {
      A(n, o), t = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function $e(e) {
  let t, s, n = (
    /*$mergedProps*/
    e[0].visible && Y(e)
  );
  return {
    c() {
      n && n.c(), t = J();
    },
    l(o) {
      n && n.l(o), t = J();
    },
    m(o, r) {
      n && n.m(o, r), Xe(o, t, r), s = !0;
    },
    p(o, [r]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, r), r & /*$mergedProps*/
      1 && j(n, 1)) : (n = Y(o), n.c(), j(n, 1), n.m(t.parentNode, t)) : n && (Ye(), A(n, 1, 1, () => {
        n = null;
      }), Ue());
    },
    i(o) {
      s || (j(n), s = !0);
    },
    o(o) {
      A(n), s = !1;
    },
    d(o) {
      o && Ge(t), n && n.d(o);
    }
  };
}
function et(e, t, s) {
  const n = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = B(t, n), r, i, c, u, a, {
    $$slots: m = {},
    $$scope: g
  } = t, {
    gradio: d
  } = t, {
    props: l = {}
  } = t;
  const _ = b(l);
  P(e, _, (f) => s(17, a = f));
  let {
    _internal: p = {}
  } = t, {
    as_item: E
  } = t, {
    visible: w = !0
  } = t, {
    elem_id: I = ""
  } = t, {
    elem_classes: R = []
  } = t, {
    elem_style: O = {}
  } = t;
  const K = Z();
  P(e, K, (f) => s(16, u = f));
  const [q, se] = Ce({
    gradio: d,
    props: a,
    _internal: p,
    visible: w,
    elem_id: I,
    elem_classes: R,
    elem_style: O,
    as_item: E,
    restProps: o
  });
  P(e, q, (f) => s(0, i = f));
  const M = he(), z = ge();
  P(e, z, (f) => s(14, r = f));
  const {
    selections: D
  } = Me(["selections"]);
  P(e, D, (f) => s(15, c = f));
  const re = ze();
  return e.$$set = (f) => {
    t = H(H({}, t), He(f)), s(23, o = B(t, n)), "gradio" in f && s(6, d = f.gradio), "props" in f && s(7, l = f.props), "_internal" in f && s(8, p = f._internal), "as_item" in f && s(9, E = f.as_item), "visible" in f && s(10, w = f.visible), "elem_id" in f && s(11, I = f.elem_id), "elem_classes" in f && s(12, R = f.elem_classes), "elem_style" in f && s(13, O = f.elem_style), "$$scope" in f && s(18, g = f.$$scope);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*props*/
    128 && _.update((f) => ({
      ...f,
      ...l
    })), se({
      gradio: d,
      props: a,
      _internal: p,
      visible: w,
      elem_id: I,
      elem_classes: R,
      elem_style: O,
      as_item: E,
      restProps: o
    }), e.$$.dirty & /*$mergedProps, $slotKey, $selectionsItems, $slots*/
    114689) {
      const f = ie(i);
      re(u, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: Le(i.elem_classes, "ms-gr-antd-table-row-selection"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...f,
          selections: i.props.selections || i.restProps.selections || ee(c),
          onCell: N(i.props.onCell || i.restProps.onCell),
          getCheckboxProps: N(i.props.getCheckboxProps || i.restProps.getCheckboxProps),
          renderCell: N(i.props.renderCell || i.restProps.renderCell),
          columnTitle: i.props.columnTitle || i.restProps.columnTitle
        },
        slots: {
          ...r,
          columnTitle: {
            el: r.columnTitle,
            callback: M,
            clone: !0
          },
          renderCell: {
            el: r.renderCell,
            callback: M,
            clone: !0
          }
        }
      });
    }
  }, [i, _, K, q, z, D, d, l, p, E, w, I, R, O, r, c, u, a, g, m];
}
class rt extends De {
  constructor(t) {
    super(), Qe(this, t, et, $e, Ze, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), h();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), h();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), h();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), h();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), h();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), h();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), h();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), h();
  }
}
export {
  rt as default
};
