package org.osmdroid.views.overlay;

import java.util.List;

import org.osmdroid.ResourceProxy;
import org.osmdroid.api.IGeoPoint;
import org.osmdroid.views.MapView;
import org.osmdroid.views.MapView.Projection;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Point;
import android.view.MotionEvent;

/**
 * Draws a list of {@link FeatureOverlay} as overlays to a map.
 * 
 * @author <a href="mailto:sebastien.grimault@makina-corpus.com">S. Grimault</a>
 *
 */
public class GroupFeatureOverlay extends FeatureOverlay
{
	//private static final Logger logger = LoggerFactory.getLogger(GroupFeatureOverlay.class);
	
	private List<FeatureOverlay> mOverlayList;
	private OnItemGestureListener mOnItemGestureListener;
	private final Point mTouchScreenPoint = new Point();
	
	public GroupFeatureOverlay(final Context ctx, final List<FeatureOverlay> pList, final OnItemGestureListener pOnItemGestureListener)
	{
		super(ctx);
		mOverlayList = pList;
		mOnItemGestureListener = pOnItemGestureListener;
	}

	public GroupFeatureOverlay(ResourceProxy pResourceProxy, final List<FeatureOverlay> pList, final OnItemGestureListener pOnItemGestureListener)
	{
		super(pResourceProxy);
		mOverlayList = pList;
		mOnItemGestureListener = pOnItemGestureListener;
	}

	public FeatureOverlay get(final int pIndex)
	{
		return mOverlayList.get(pIndex);
	}

	public void add(final FeatureOverlay pElement)
	{
		mOverlayList.add(pElement);
	}
	
	public void clear()
	{
		mOverlayList.clear();
	}
	
	@Override
	public boolean onSingleTapUp(MotionEvent event, MapView mapView)
	{
		//logger.info("onSingleTapUp : " + event.toString());
		
		return (activateSelectedItems(event, mapView, new ActiveOverlay()
		{
			@Override
			public boolean performTask(int index)
			{
				final GroupFeatureOverlay that = GroupFeatureOverlay.this;
				
				if (that.mOnItemGestureListener == null)
				{
					return false;
				}
				
				return that.mOnItemGestureListener.onItemSingleTapUp(index, that.mOverlayList.get(index));
			}
		})) ? true : super.onSingleTapUp(event, mapView);
	}

	@Override
	protected void draw(final Canvas c, final MapView pMapView, final boolean shadow)
	{
		for (final Overlay overlay : mOverlayList)
		{
			if (overlay.isEnabled())
			{
				overlay.draw(c, pMapView, true);
			}
		}

		for (final Overlay overlay : mOverlayList)
		{
			if (overlay.isEnabled())
			{
				overlay.draw(c, pMapView, false);
			}
		}
	}

	@Override
	protected boolean hitTest(Point pHitPoint)
	{
		return false;
	}
	
	/**
	 * When a content sensitive action is performed the overlay needs to be identified.
	 * This method does that and then performs the assigned task on that overlay.
	 *
	 * @param event
	 * @param mapView
	 * @param task
	 * @return <code>true</code> if event is handled, <code>false</code> otherwise
	 */
	private boolean activateSelectedItems(final MotionEvent event, final MapView mapView, final ActiveOverlay task)
	{
		final Projection pj = mapView.getProjection();
		final int eventX = (int) event.getX();
		final int eventY = (int) event.getY();

		// These objects are created to avoid construct new ones every cycle
		IGeoPoint gPoint = pj.fromPixels(eventX, eventY);
		pj.toMapPixelsProjected(gPoint.getLatitudeE6(), gPoint.getLongitudeE6(), mTouchScreenPoint);
		
		for (int i = 0; i < this.mOverlayList.size(); ++i)
		{
			final FeatureOverlay item = this.mOverlayList.get(i);
			
			if (item.hitTest(mTouchScreenPoint))
			{
				if (task.performTask(i))
				{
					return true;
				}
			}
		}
		return false;
	}
	
	public static interface ActiveOverlay
	{
		public boolean performTask(final int index);
	}
	
	/**
	 * When an overlay is touched, one of these methods may be invoked depending on the type of touch.
	 *
	 * Each of them returns <code>true</code> if the event was completely handled.
	 */
	public static interface OnItemGestureListener
	{
		public boolean onItemSingleTapUp(final int index, final FeatureOverlay overlay);
		public boolean onItemLongPress(final int index, final FeatureOverlay overlay);
	}
}
