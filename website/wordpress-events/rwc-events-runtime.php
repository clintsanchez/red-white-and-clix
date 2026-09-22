<?php
/** Event presentation helpers. Meta Box owns the content type and field schema. */
defined('ABSPATH') || exit;

add_action('pre_get_posts', static function ($query) {
    if (is_admin() || !$query->is_main_query() || !$query->is_post_type_archive('rwc_event')) return;
    $query->set('posts_per_page', 9);
    $query->set('meta_query', [
        'relation' => 'OR',
        'event_start' => ['key' => 'rwc_event_start', 'compare' => 'EXISTS', 'type' => 'DATETIME'],
        'undated' => ['key' => 'rwc_event_start', 'compare' => 'NOT EXISTS'],
    ]);
    $query->set('orderby', ['event_start' => 'ASC', 'ID' => 'ASC']);
});

add_filter('elementor/frontend/widget/should_render', static function ($render, $widget) {
    if (get_post_type() !== 'rwc_event' || $widget->get_name() !== 'button') return $render;
    $tag = $widget->get_settings('__dynamic__')['link'] ?? '';
     $key = '';
    foreach (['registration_url', 'map_url', 'rules_url', 'online_url'] as $field) {
        if (strpos($tag, 'rwc_event_' . $field) !== false) $key = 'rwc_event_' . $field;
    }
    if (!$key) return $render;
    $url = get_post_meta(get_the_ID(), $key, true);
    if ($key !== 'rwc_event_registration_url') return $render && (bool) wp_http_validate_url($url);
    $status = get_post_meta(get_the_ID(), 'rwc_event_status', true);
    return $render && (bool) wp_http_validate_url($url)
        && !in_array($status, ['Cancelled', 'Postponed', 'Sold out', 'Completed'], true);
}, 10, 2);

add_filter('elementor/widget/render_content', static function ($html, $widget) {
    if (get_post_type() !== 'rwc_event') return $html;
    $dynamic = wp_json_encode($widget->get_settings('__dynamic__'));
    foreach (['start', 'end', 'registration_deadline'] as $field) {
        $key = 'rwc_event_' . $field;
        if (strpos($dynamic, $key) === false) continue;
        $raw = get_post_meta(get_the_ID(), $key, true);
        if (!$raw) continue;
        try {
            $zone = new DateTimeZone(get_post_meta(get_the_ID(), 'rwc_event_timezone', true) ?: wp_timezone_string());
            $date = DateTimeImmutable::createFromFormat('!Y-m-d H:i:s', $raw, $zone);
            if ($date) $html = str_replace(esc_html($raw), esc_html(wp_date('F j, Y · g:i a T', $date->getTimestamp(), $zone)), $html);
        } catch (Exception $e) {
            // Preserve the entered value if an editor has not yet supplied a valid timezone.
        }
    }
    return $html;
}, 10, 2);
