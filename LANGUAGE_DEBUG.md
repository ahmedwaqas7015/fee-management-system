# Language Support Debugging Guide

## Current Status

✅ **Translations are compiled correctly:**
- Urdu .mo file: 7.5KB (104 messages)
- English .mo file: 445 bytes
- Translation directory: `/home/logixsy/learning/tasks/fms/translations` ✅

✅ **Locale selector is working:**
- When session['language'] = 'en', get_locale() returns 'en' ✅
- When session['language'] = 'ur', get_locale() returns 'ur' ✅
- Translations work: "Students" → "طلباء" (Urdu) ✅

## Potential Issues

### 1. **Session Not Persisting**
- **Symptom**: Language switches but reverts on page reload
- **Fix**: Already added `session.permanent = True` in `change_language` route

### 2. **Browser Cache**
- **Symptom**: Old translations showing
- **Fix**: Clear browser cache and cookies

### 3. **Template Context Variable**
- **Symptom**: RTL/LTR direction changes but text stays English
- **Issue**: `current_language` in templates might not match Flask-Babel's locale
- **Fix**: Use `get_locale()` from Flask-Babel in context processor

## Testing Steps

1. **Start the app:**
   ```bash
   python run.py
   ```

2. **Open browser and login**

3. **Check default language:**
   - Should be Urdu (RTL)
   - Text should be in Urdu

4. **Switch to English:**
   - Click language dropdown
   - Select "English"
   - Page should reload
   - Text should change to English (LTR)

5. **Switch back to Urdu:**
   - Click language dropdown  
   - Select "اردو"
   - Page should reload
   - Text should change to Urdu (RTL)

## If Still Not Working

Check browser console for:
- Session cookie being set
- Any JavaScript errors
- Network requests to language switcher

Check Flask logs for:
- Locale selector being called
- Session values
