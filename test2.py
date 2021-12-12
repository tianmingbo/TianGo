1 != T.needShowNewVc | | T.hasVCSuccess ? 1 == T.needShowNewVc & & T.hasVCSuccess ?
(e = T.checkUrl.replace( / ^ https?:\ / \ // gi, '').split('/')[0], T.show_err(
    '网络遇到点问题，请稍后刷新页面重试。<a target="_blank" href="https://ping.huatuo.qq.com/' + e + '">点击排查。</a>', !0), S.logger.info(
    '$login_btn.onClick()', 'plogin.cntCheckTimeout='.concat(T.cntCheckTimeout))): T.submit(t): (
    T.showVC(), S.logger.info('$login_btn.onClick()', 'showVC'))
