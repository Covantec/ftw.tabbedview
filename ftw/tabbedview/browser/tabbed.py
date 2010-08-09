from Products.CMFCore.Expression import getExprContext
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TabbedView(BrowserView):
    """A View containing tabs with fancy ui"""

    __call__ = ViewPageTemplateFile("tabbed.pt")

    def get_tabs(self):
        """Returns a list of dicts containing the tabs definitions"""
        for action, icon in self.get_actions(category='tabbedview-tabs'):
            css_classes = None
            #get the css classes that should be set on the A elements.
            view_name = "tabbedview_view-%s" % action['id']
            view = self.context.restrictedTraverse(view_name)
            if view and hasattr(view, 'get_css_classes'):
                css_classes = ' '.join(view.get_css_classes())
            yield {
                'id': action['id'].lower(),
                'icon': icon,
                'url': action['url'],
                'class': css_classes,
                }

    def get_actions(self, category=''):
        """Returns the available and visible types actions
        in the given category
        """
        context = self.context
        types_tool = getToolByName(context, 'portal_types')
        ai_tool = getToolByName(context, 'portal_actionicons')
        actions = types_tool.listActions(object=context)
        for action in actions:
            if action.category == category:
                icon = ai_tool.queryActionIcon(action_id=action.id,
                                                category=category,
                                                context=context)
                econtext = getExprContext(context, context)
                action = action.getAction(ec=econtext)
                if action['available'] and action['visible']:
                    yield action, icon

    def listing(self):
        """Fetches the corresponding view which renders a listing.
        Called from javascript tabbedview.js in reload_view line 58
        """
        view_name = self.request.get('view_name', None)
        if view_name:
            listing_view = queryMultiAdapter((self.context, self.request),
                            name='tabbedview_view-%s' % view_name)
            if listing_view is None:
                listing_view = queryMultiAdapter((self.context, self.request),
                                name='tabbedview_view-fallback')
            return listing_view()

    def select_all(self):
        """Returns a list of all Objects machting the search parameters.
        Called from javascript tabbedview.js in select_all line 186
        """
        # TODO: reimplement functionality copied from views.SelectAllView
        pass
        # self.tab = self.context.restrictedTraverse("tabbedview_view-%s" %
        #                                   self.request.get('view_name'))
        # self.tab.update()
        #
        # return super(SelectAllView, self).__call__()