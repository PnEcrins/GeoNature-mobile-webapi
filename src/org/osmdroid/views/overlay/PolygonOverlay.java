package org.osmdroid.views.overlay;

import java.util.ArrayList;
import java.util.List;

import org.osmdroid.DefaultResourceProxyImpl;
import org.osmdroid.ResourceProxy;
import org.osmdroid.util.GeoPoint;
import org.osmdroid.views.MapView;
import org.osmdroid.views.MapView.Projection;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Point;
import android.graphics.Rect;

/**
 * Describe a Polygon as overlay.
 * 
 * @author <a href="mailto:sebastien.grimault@makina-corpus.com">S. Grimault</a>
 *
 */
public class PolygonOverlay extends FeatureOverlay
{
	//private static final Logger logger = LoggerFactory.getLogger(PolygonOverlay.class);
	
	/**
	 * Stores points, converted to the map projection.
	 */
	private List<Point> mPoints;

	/**
	 * Number of points that have precomputed values.
	 */
	private int mPointsPrecomputed;

	/**
	 * Paint settings.
	 */
	protected Paint mPaint = new Paint();

	private final Path mPath = new Path();

	private final Point mTempPoint1 = new Point();
	private final Point mTempPoint2 = new Point();

	// bounding rectangle for the current line segment.
	private final Rect mLineBounds = new Rect();
	
	public PolygonOverlay(int color, Context ctx)
	{
		this(color, new DefaultResourceProxyImpl(ctx));
	}

	public PolygonOverlay(int color, ResourceProxy pResourceProxy)
	{
		super(pResourceProxy);
		
		mPaint = new Paint();
		mPaint.setColor(color);
		mPaint.setStrokeWidth(2.0f);
		mPaint.setAntiAlias(true);
		mPaint.setStyle(Paint.Style.STROKE);
		mPaint.setAlpha(128);
		
		this.clearPath();
	}

	public void setColor(final int color)
	{
		this.mPaint.setColor(color);
	}

	public void setAlpha(final int a)
	{
		this.mPaint.setAlpha(a);
	}

	public Paint getPaint()
	{
		return mPaint;
	}

	public void setPaint(final Paint pPaint)
	{
		if (pPaint == null)
		{
			throw new IllegalArgumentException("pPaint argument cannot be null");
		}
		
		mPaint = pPaint;
	}

	public void clearPath()
	{
		this.mPoints = new ArrayList<Point>();
		this.mPointsPrecomputed = 0;
	}

	public void addPoint(final GeoPoint pt)
	{
		this.addPoint(pt.getLatitudeE6(), pt.getLongitudeE6());
	}

	public void addPoint(final int latitudeE6, final int longitudeE6)
	{
		this.mPoints.add(new Point(latitudeE6, longitudeE6));
	}

	public int getNumberOfPoints()
	{
		return this.mPoints.size();
	}

	@Override
	protected void draw(Canvas canvas, MapView mapView, boolean shadow)
	{
		if (shadow)
		{
			return;
		}

		if (this.mPoints.size() < 3)
		{
			// nothing to paint
			return;
		}

		final Projection pj = mapView.getProjection();

		// precompute new points to the intermediate projection.
		final int size = this.mPoints.size();

		while (this.mPointsPrecomputed < size)
		{
			final Point pt = this.mPoints.get(this.mPointsPrecomputed);
			pj.toMapPixelsProjected(pt.x, pt.y, pt);

			this.mPointsPrecomputed++;
		}
		
		// points on screen
		Point screenPoint0 = null;
		Point screenPoint1 = null;
		
		// points from the points list
		Point projectedPoint0;
		Point projectedPoint1;

		// clipping rectangle in the intermediate projection, to avoid performing projection.
		final Rect clipBounds = pj.fromPixelsToProjected(pj.getScreenRect());

		mPath.rewind();
		projectedPoint0 = this.mPoints.get(size - 1);
		mLineBounds.set(projectedPoint0.x, projectedPoint0.y, projectedPoint0.x, projectedPoint0.y);

		for (int i = size - 2; i >= 0; i--)
		{
			// compute next points
			projectedPoint1 = this.mPoints.get(i);
			mLineBounds.union(projectedPoint1.x, projectedPoint1.y);

			if (!Rect.intersects(clipBounds, mLineBounds))
			{
				// skip this line, move to next point
				projectedPoint0 = projectedPoint1;
				screenPoint0 = null;
				continue;
			}

			// the starting point may be not calculated, because previous segment was out of clip bounds
			if (screenPoint0 == null)
			{
				screenPoint0 = pj.toMapPixelsTranslated(projectedPoint0, this.mTempPoint1);
				mPath.moveTo(screenPoint0.x, screenPoint0.y);
			}

			screenPoint1 = pj.toMapPixelsTranslated(projectedPoint1, this.mTempPoint2);

			// skip this point, too close to previous point
			if (Math.abs(screenPoint1.x - screenPoint0.x) + Math.abs(screenPoint1.y - screenPoint0.y) <= 1)
			{
				continue;
			}

			mPath.lineTo(screenPoint1.x, screenPoint1.y);

			// update starting point to next position
			projectedPoint0 = projectedPoint1;
			screenPoint0.x = screenPoint1.x;
			screenPoint0.y = screenPoint1.y;
			mLineBounds.set(projectedPoint0.x, projectedPoint0.y, projectedPoint0.x, projectedPoint0.y);
		}

		canvas.drawPath(mPath, this.mPaint);
	}

	@Override
	protected boolean hitTest(Point pHitPoint)
	{
		boolean result = false;
		
		if (pHitPoint != null)
		{
			Point p1 = mPoints.get(0);
			
			for (int i = 1; i < mPoints.size(); i++)
			{
				Point p2 = mPoints.get(i);
				
				if (((p2.x <= pHitPoint.x && pHitPoint.x < p1.x) ||
					(p1.x <= pHitPoint.x && pHitPoint.x < p2.x)) &&
					(pHitPoint.y < (p1.y - p2.y) * (pHitPoint.x - p2.x) / (p1.x - p2.x) + p2.y))
				{
					result = !result;
				}
				
				p1 = p2;
			}
		}
		
		return result;
	}
}
